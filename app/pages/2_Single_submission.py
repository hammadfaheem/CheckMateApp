import streamlit as st
import pandas as pd
import os
import sys
from PyPDF2 import PdfReader
import docx
from code import PlagiarismDetector
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize



# Get the absolute path of the project root (ASSIGNMENT_CHACK)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)  # Add project root to sys.path

from agents import (FormatAgent, RubricAgent, EvaluatorAgent, RubricAgentTeacherQuestion)

def extract_text(file_obj):
    # Determine the file name for extension extraction.
    if hasattr(file_obj, 'name'):
        file_name = file_obj.name
    else:
        file_name = file_obj

    ext = os.path.splitext(file_name)[1].lower()

    if ext == '.pdf':
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
        reader = PdfReader(file_obj)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.split("\n")
    
    elif ext in ['.doc', '.docx']:
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
        document = docx.Document(file_obj)
        full_text = [para.text for para in document.paragraphs]
        return full_text

    elif ext == '.txt':
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
        content = file_obj.read()
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        return content.splitlines()
    
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

# Input Sample Texts
# student_raw_text ="""The OSI model in networking is a conceptual framework used to understand and standardize the functions of a communication system. It consists of seven layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application.
# A router is a device that forwards data packets between computer networks, while a switch operates at a local level to connect devices within a single network.
# Firewalls are crucial for network security because they monitor and control incoming and outgoing network traffic based on security rules, helping prevent unauthorized access and attacks."""

# teacher_questions = """1. What is the OSI model in networking? marks 5
# 2. What are the differences between a router and a switch? marks 5
# 3. Explain the importance of firewalls in network security. marks 5"""

# teacher_raw_text = """
# 1. The OSI (Open Systems Interconnection) model is a conceptual framework used to standardize network communication. It consists of seven layers: 
#    - **Physical Layer**: Handles the physical connection between devices.  
#    - **Data Link Layer**: Manages node-to-node communication and error detection.  
#    - **Network Layer**: Handles routing and forwarding of data packets.  
#    - **Transport Layer**: Ensures reliable transmission of data between systems.  
#    - **Session Layer**: Manages sessions and connections between applications.  
#    - **Presentation Layer**: Translates data formats and encryption.  
#    - **Application Layer**: Provides network services to end-users.

# 2. A **router** and a **switch** serve different functions in networking:
#    - A **router** operates at the **network layer (Layer 3)** and is responsible for forwarding data between different networks using IP addresses.  
#    - A **switch** operates at the **data link layer (Layer 2)** and is used within a local network (LAN) to connect devices efficiently using MAC addresses.  
#    - Routers enable communication between networks (e.g., connecting to the internet), while switches improve network efficiency within a single network.

# 3. Firewalls play a critical role in **network security** by:
#    - Monitoring and controlling **incoming and outgoing traffic** based on predefined security rules.  
#    - Preventing **unauthorized access** by blocking malicious traffic.  
#    - Acting as a barrier between a **trusted internal network** and **untrusted external sources**, reducing the risk of cyber threats.  
#    - Implementing security policies such as **packet filtering, intrusion detection, and deep packet inspection** to safeguard sensitive data.
# """

## Streamlit UI - Improved Version with Expanders

st.title("📚 **Assignment Grading & Feedback for Single Student**")

# Add some visual style
st.markdown("<style> .css-1d391kg {background-color: #f3f3f3;} </style>", unsafe_allow_html=True)

# Step 1: Questions Input
with st.expander("Step 1: Enter Questions"):
    method = st.radio("Input Method:", ("Text Field", "Upload File"), key="q_method", index=0)
    if method == "Text Field":
        # questions_text = st.text_area("Enter questions (one per line):", value=teacher_questions, height=150)
        questions_text = st.text_area("Enter questions (one per line):",  height=150)
        questions = questions_text.split("\n") if questions_text else []
    else:
        file = st.file_uploader("Upload TXT, DOC, or PDF", type=["txt", "docx", "pdf"])
        questions = extract_text(file) if file else []

# Step 2: Answer Key Input
with st.expander("Step 2: Enter Answer Key"):
    method = st.radio("Input Method:", ("Text Field", "Upload File"), key="a_method", index=0)
    if method == "Text Field":
        # answer_key_text = st.text_area("Enter answers (one per line):", value=teacher_raw_text, height=150)
        answer_key_text = st.text_area("Enter answers (one per line):", height=150)
        answer_key = answer_key_text.split("\n") if answer_key_text else []
    else:
        file = st.file_uploader("Upload Answer Key File", type=["txt", "docx", "pdf"])
        answer_key = extract_text(file) if file else []

# Step 3: Student Answers Input
with st.expander("Step 3: Enter Student Answers"):
    method = st.radio("Input Method:", ("Text Field", "Upload File"), key="s_method", index=0)
    if method == "Text Field":
        # student_answers_text = st.text_area("Enter student answers:", value=student_raw_text, height=150)
        student_answers_text = st.text_area("Enter student answers:", height=150)
        student_answers = student_answers_text.split("\n") if student_answers_text else []
    else:
        file = st.file_uploader("Upload Student Answers", type=["txt", "docx", "pdf"])
        student_answers = extract_text(file) if file else []


# Step 4: Total Marks
total_marks = st.number_input("Total Marks:", min_value=1, max_value=100, value=10, step=1, label_visibility="collapsed")

# Answer Evaluation
if st.button("Check Answers", use_container_width=True):
    format_agent = FormatAgent()
    rubric_agent = RubricAgent()
    evaluator_agent = EvaluatorAgent()
    rubric_agent_teacher_question = RubricAgentTeacherQuestion()
    plagiarism_detector = PlagiarismDetector()

    # print(student_answers)
    # if (student_answers) == list:
    #     result, perplexity, burstiness = plagiarism_detector.classify_text("\n".join(student_raw_text))
    # else:


    questions = " ".join(questions).replace("\n", " ")
    answer_key = " ".join(answer_key).replace("\n", " ")
    student_answers = " ".join(student_answers).replace("\n", " ")

    result, perplexity, burstiness = plagiarism_detector.classify_text(student_answers)


    student_formatted, teacher_formatted = format_agent.get_response(
        teacher_questions=answer_key, teacher_raw_text=questions, student_raw_text=student_answers
    )

    rubric_response = rubric_agent_teacher_question.get_response(questions)
    if rubric_response == {}:
        rubric_response = rubric_agent.get_response(answer_key, total_marks)

    data = evaluator_agent.get_response(student_formatted, teacher_formatted, rubric_response)

    # Add some style
    st.markdown("<hr>", unsafe_allow_html=True)

    # Evaluation Summary and Columns Layout
    st.subheader("🎯 **Evaluation Summary**")
    st.write(data["chain_of_thought"])

    # Create columns for the four sections
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("📝 Student Text")
        st.write(student_answers)

    with col2:
        st.subheader("💯 Marks")
        df = pd.DataFrame(data["marks"].items(), columns=["Question", "Marks"])
        df["Total Marks"] = rubric_response.values()
        st.dataframe(df, hide_index=True)

    with col3:
        st.subheader("💬 Personalized Feedback")
        st.write(data["personalized_feedback"])

    with col4:
        st.subheader("🔍 Plagiarism Detection")
        st.write(result)

else:
    st.info("Click 'Check Answers' to evaluate. 👇", icon="🔍")