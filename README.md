AI-Powered Government Schemes Chatbot
Welcome to the AI-Powered Government Schemes Chatbot repository! This project develops a chatbot to assist students and parents in navigating government schemes, scholarships, and financial aid programs at state and national levels. The chatbot provides personalized recommendations, guides users through application processes, and sends timely notifications for deadlines.
Live demo: https://aipowered-govt-schemes.streamlit.app/
Project Overview
The chatbot leverages Large Language Models (LLMs) and the Retrieval-Augmented Generation (RAG) pattern to offer a seamless experience. It collects user details (e.g., age, income, education level, state), matches them with eligible schemes, and provides step-by-step application guidance. Key features include:

Personalized Recommendations: Suggests schemes based on user profiles using a RAG-based knowledge base.
Application Guidance: Answers queries and provides document checklists and deadlines.
Timely Notifications: Sends email/SMS reminders for upcoming deadlines.
Multilingual Support: Supports multiple regional languages.
User-Friendly Interface: Hosted on Streamlit for easy access.

Setup Instructions
Prerequisites

Python 3.11 or higher
Git
A code editor (e.g., PyCharm, Jupyter Notebook, VS Code)

Installation

Clone the Repository  
git clone https://github.com/surajpandey111/AI_Powered_Schemes.git
cd AI_Powered_Schemes


Set Up a Virtual Environment  
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install DependenciesEnsure you have a requirements.txt file with the following:
streamlit==1.36.0
langchain==0.2.5
faiss-cpu==1.8.0
pymongo==4.7.3

Then install:
pip install -r requirements.txt


Run the App Locally  
streamlit run app.py

The app will open in your default browser at http://localhost:8501.


Usage

Open the app locally or visit the live demo: https://aipowered-govt-schemes.streamlit.app/.
Enter your details (e.g., "I’m a 10th-grade student from Maharashtra") in the input field.
The chatbot will respond with relevant schemes, eligibility criteria, and application steps.
Check the "Proof of Work" section on the app for a screenshot of the chatbot in action.

Proof of Work
The chatbot has been tested and deployed successfully. Below is a screenshot demonstrating its functionality, where it recommends the UP Scholarship for a 10th-grade student from Maharashtra:

Team Participants

Suraj Kumar Pandey(Team Leader)
Kritika Pandey
Divyansh Vishwakarma
Rajeev Rajesh

Contributing
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. For major updates, open an issue first to discuss your ideas.
Links

GitHub Repository: https://github.com/surajpandey111/AI_Powered_Schemes
Live Demo: https://aipowered-govt-schemes.streamlit.app/

License
This project is licensed under the MIT License. See the LICENSE file for details.
