import streamlit as st
import pandas as pd
import zipfile
import io
import os
import tempfile
from PyPDF2 import PdfReader
from difflib import SequenceMatcher
import docx
import sys

# Get the absolute path of the project root (ASSIGNMENT_CHACK)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)  # Add project root to sys.path

from agents import (FormatAgent,
                    RubricAgent,
                    EvaluatorAgent,
                    RubricAgentTeacherQuestion)

# Function to extract text from files (PDF, DOCX, TXT)
def extract_text(file_obj):
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
    
def find_similarity_search(students_answers):
    similarity_data = []
    for name1 in students_answers.keys():
        for name2 in students_answers.keys():
            if name1 != name2:
                similarity = SequenceMatcher(
                    None, 
                    students_answers[name1],
                    students_answers[name2]
                ).quick_ratio()
                rec = [name1, name2, similarity]
                similarity_data.append(rec)
    return similarity_data

# Function to process a zip file and evaluate each student answer
def process_zip_file(zip_file, answer_key, questions, rubric_response, total_marks):
    results = []  # List to store evaluation results for each file

    # Create a temporary directory to extract zip contents
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Save and extract the zip file into the temporary directory
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)
        
        # Initialize agents outside of the loop
        format_agent = FormatAgent()
        evaluator_agent = EvaluatorAgent()

        student_answers = {}

        # Walk through the temporary directory and process each file
        for root, dirs, files in os.walk(tmpdirname):
            for filename in files:
                file_path = os.path.join(root, filename)
                with open(file_path, 'rb') as f:
                    student_answer = extract_text(f)

                student_answers[filename] = student_answer
                # Process evaluation using your agents
                student_formatted, teacher_formatted = format_agent.get_response(
                    teacher_questions=answer_key, 
                    teacher_raw_text=questions, 
                    student_raw_text=student_answer
                )

                # Use the precomputed rubric response for all students
                data = evaluator_agent.get_response(student_formatted, teacher_formatted, rubric_response)
                
                # Compute total marks from individual question marks
                obtained_marks = sum(data["marks"].values())
                
                # Save results for this student file
                results.append({
                    "file_name": filename,
                    "assignment_marks": obtained_marks,
                    "evaluation_process": data["chain_of_thought"],
                    "personalized_feedback": data["personalized_feedback"]
                })
                

                # Remove the processed file from the temporary folder
                os.remove(file_path)
    
    # Note: When the 'with' block ends, the temporary directory and any remaining files are removed.
    return results, student_answers

##############################################
# User Interface with Streamlit

st.title("📚 Bulk Submission")

# Section 1: Questions Input
with st.expander("Step 1: Enter Questions"):
    method = st.radio("Input Method:", ("Text Field", "Upload File"), key="q_method")
    if method == "Text Field":
        questions_text = st.text_area("Enter questions (one per line):", 
                                      value="1. What is the OSI model in networking?\n2. What are the differences between a router and a switch?\n3. Explain the importance of firewalls in network security.")
        questions = questions_text.split("\n") if questions_text else []
    else:
        file = st.file_uploader("Upload TXT, DOC, or PDF", type=["txt", "docx", "pdf"], key="q_file")
        questions = extract_text(file) if file else []

# Section 2: Answer Key Input
with st.expander("Step 2: Enter Answer Key"):
    method = st.radio("Input Method:", ("Text Field", "Upload File"), key="a_method")
    if method == "Text Field":
        answer_key_text = st.text_area("Enter answers (one per line):", 
                                       value="1. The OSI (Open Systems Interconnection) model is a conceptual framework used to standardize network communication. It consists of seven layers...\n2. A router operates at Layer 3 while a switch operates at Layer 2...\n3. Firewalls monitor and control incoming/outgoing traffic to secure the network.")
        answer_key = answer_key_text.split("\n") if answer_key_text else []
    else:
        file = st.file_uploader("Upload Answer Key File", type=["txt", "docx", "doc", "pdf"], key="a_file")
        answer_key = extract_text(file) if file else []

# Section 3: Student Answers Input (ZIP file)
with st.expander("Step 3: Upload Student Answers (ZIP file)"):
    uploaded_zip = st.file_uploader("Upload ZIP file containing student answers", type=["zip"], key="s_zip")
    
# Section 4: Total Marks Input
total_marks = st.number_input("Total Marks:", min_value=1, max_value=100, value=10, step=1)

# Container for output CSV download
output_csv = None

# Answer Evaluation
if st.button("Check Answers"):

    format_agent = FormatAgent()
    rubric_agent = RubricAgent()
    evaluator_agent = EvaluatorAgent()
    rubric_agent_teacher_question = RubricAgentTeacherQuestion()

    if not uploaded_zip:
        st.error("Please upload a ZIP file with student answers.")
    else:
        # Calculate the rubric only once, using the answer key
        rubric_response = rubric_agent.get_response(answer_key, total_marks)
        rubric_response = rubric_agent_teacher_question.get_response(questions)
        if rubric_response == {}:
            rubric_response = rubric_agent.get_response(answer_key, total_marks)
        
        # Process the ZIP file and get results for each student file
        results , student_answers = process_zip_file(uploaded_zip, answer_key, questions, rubric_response, total_marks)
        similarity_data = find_similarity_search(student_answers)
        
        if results:
            st.success("Evaluation complete for all student files!")
            
            # Create a DataFrame from the results
            df_results = pd.DataFrame(results)
            similarity_df = pd.DataFrame(similarity_data, columns=["Student 1", "Student 2", "Similarity"])

            # Show the DataFrame as a table in Streamlit
            st.subheader("Evaluation Results")
            st.dataframe(df_results, use_container_width=True)

            st.subheader("Similarity Search")
            st.dataframe(similarity_df, use_container_width=True)

            # Create a CSV output file for downloading
            csv_buffer = io.StringIO()
            df_results.to_csv(csv_buffer, index=False)
            output_csv = csv_buffer.getvalue()
            
            st.download_button(
                label="Download Evaluation Results as CSV",
                data=output_csv,
                file_name="evaluation_results.csv",
                mime="text/csv",
            )
        else:
            st.info("No student files were found in the ZIP archive.")
else:
    st.info("Click 'Check Answers' to evaluate.")
