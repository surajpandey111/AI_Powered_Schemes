import streamlit as st
import os
import google.generativeai as genai
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from datetime import datetime, timedelta
import re


genai.configure(api_key=os.getenv("GEMINI_API_KEY", "your-actual-api-key"))
gemini = genai.GenerativeModel("gemini-2.5-flash-lite")


def load_and_split_documents():
    loader = TextLoader("UP Scholarship Scheme.txt")
    docs = loader.load()
    
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=2000,
        chunk_overlap=200
    )
    return text_splitter.split_documents(docs)


@st.cache_resource
def embed_documents(_docs):
    texts = [doc.page_content for doc in _docs]
    embedding_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    db = FAISS.from_texts(texts, embedding=embedding_model, metadatas=[{"text": text} for text in texts])
    return db


def extract_deadlines(docs):
    deadlines = []
    for doc in docs:
        content = doc.page_content
        if "Important Dates:" in content:
            try:
                app_period = re.search(r"Application Period: (.*?) to (.*?)(?:\n|$)", content)
                if app_period:
                    end_date_str = app_period.group(2).strip()
                    try:
                        if "Ongoing" in end_date_str or "Varies" in end_date_str or "within" in end_date_str:
                            continue
                        else:
                            end_date = datetime.strptime(end_date_str, "%dth %B %Y")
                    except ValueError:
                        try:
                            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                        except ValueError:
                            continue
                    scheme_name = re.search(r"^(.*?)\n", content).group(1).strip()
                    deadlines.append((scheme_name, end_date))
            except (IndexError, ValueError):
                continue
    return deadlines


def send_email_reminder(email, scheme_name, deadline):
    st.write(f"📧 Simulated Email to {email}: Reminder! The deadline for {scheme_name} is {deadline.strftime('%Y-%m-%d')}.")


docs = load_and_split_documents()
db = embed_documents(docs)


deadlines = extract_deadlines(docs)


st.title("📚 AI-Powered Chatbot for Government Schemes & Financial Aid")
st.write("I can help you navigate government schemes, scholarships, and financial aid programs. Ask me anything!")


st.sidebar.header("🔔 Upcoming Deadlines")
today = datetime(2025, 5, 25)
for scheme_name, deadline in sorted(deadlines, key=lambda x: x[1]):
    days_left = (deadline - today).days
    if 0 <= days_left <= 30:
        st.sidebar.warning(f"⏰ {scheme_name}: {deadline.strftime('%Y-%m-%d')} ({days_left} days left)")


user_email = st.sidebar.text_input("Enter your email for reminders:")
if user_email and st.sidebar.button("Set Reminder"):
    for scheme_name, deadline in deadlines:
        days_left = (deadline - today).days
        if 0 <= days_left <= 30:
            send_email_reminder(user_email, scheme_name, deadline)


user_input = st.text_input("Your Question:", placeholder="E.g., What scholarships am I eligible for?")
if user_input:
    user_input_lower = user_input.lower().strip()
    if any(phrase in user_input_lower for phrase in ["who are you", "what are you", "who is this", "what is this"]):
        st.markdown("### 🧠 Answer:\nI am an AI-powered chatbot here to assist you with government schemes, scholarships, and financial aid!")
    else:
        
        search_results = db.similarity_search_with_score(user_input, k=10)
        context = "\n\n".join([doc.page_content for doc, _ in search_results])

        
        prompt = f"Use the following context to answer the question in detail, including eligibility, benefits, required documents, and application process:\n\n{context}\n\nQuestion: {user_input}"

        try:
            response = gemini.generate_content(prompt)
            st.markdown(f"### 🧠 Answer:\n{response.text}")
        except Exception as e:
            st.error(f"❌ Gemini Error: {e}")

    
    if "eligible" in user_input_lower or "scholarship" in user_input_lower:
        st.markdown("### 🎯 Recommended Schemes:")
        relevant_docs = db.similarity_search(user_input, k=5)
        for doc in relevant_docs:
            scheme_name = doc.page_content.split("\n")[0].strip()
            st.write(f"- {scheme_name}")