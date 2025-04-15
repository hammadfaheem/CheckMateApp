from dotenv import load_dotenv
import os
import json
from .utils import get_chatbot_response
from openai import OpenAI
import re
load_dotenv()

class FormatAgent():
    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")
    
    def get_response(self, teacher_questions, student_raw_text, teacher_raw_text):

        system_prompt = """
        You are an AI assistant tasked with formatting student assignments based on teacher-provided questions and responses, along with the student's raw text. Your goal is to structure the student’s answers correctly in relation to the teacher's response.

        ### Instructions:
        1. Given a set of questions, a raw student response, and a teacher's response, identify the answers in the student’s text.
        2. For each question:
        - Locate the corresponding answer in the student's response.
        - Compare it with the teacher's response to ensure completeness.
        3. Return a structured list of dictionaries. Each dictionary must contain:
        - `"Question"`: The exact question provided by the teacher.
        - `"Student Answer"`: The student's response to the question.
        - `"Teacher Answer"`: The teacher's correct response for reference.
        4. If the student has not provided an answer, set the `"Student Answer"` field to an empty string or indicate "Unanswered."
        5. Ensure the output is clean and structured, with each question-answer pair correctly aligned.\\
        6. Make sure you don't miss any text in the formatted response from the teacher's response and student's response. 

        ### Format Example:
        **Teacher’s Questions:**
        1. What is the capital of France?  
        2. Who is the president of the USA?  

        **Student's Raw Text:**  
        "The capital of France is Paris."  

        **Teachers's Raw Text:**  
        "The capital of France is Paris. The USA has a leader named Biden."  

        **Teacher's Response:**  
        "The capital of France is **Paris**. The president of the USA is **Joe Biden**."  

        **Output:**
        The system will return the following JSON object, you are not alllowed to return anyhitng else other than the JSON object. and don't include this as well ```json```:
        ```json
        {
            "teacher_formated_response":[
            {
                "question1": "What is the capital of France?",
                "answer1": "The capital of France is Paris."
            },
            {
                "question2": "Who is the president of the USA?",
                "answer2": "Joe Biden is the president of the USA."
            }
            ],

            "student_formated_response": [
            {
                "question1": "What is the capital of France?",
                "answer"1: "The capital of France is Paris."
            },
            {
                "question2": "Who is the president of the USA?",
                "answer2": "Unanswered"
            }
            ]
        }
        ```
        Note : Make sure you must use  the keys names as "teacher_formated_response", "student_formated_response" and the values should be a list of dictionaries.
        """

        user_prompt = f"""
        Teacher’s Questions:
        {teacher_questions}

        Student Raw Text:
        {student_raw_text}

        Teacher Raw Text:
        {teacher_raw_text}
        """
        input_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
            ]

        output =get_chatbot_response(self.client,self.model_name,input_messages)
        student_formated_response, teacher_formated_response = self.postprocess(output)
        
        return student_formated_response, teacher_formated_response
        # return output

    def postprocess(self,output):
        # Remove the <think> section
        cleaned_text = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL)

        # Remove triple backticks and "json" label
        cleaned_text = re.sub(r"```json\s*", "", cleaned_text)
        cleaned_text = re.sub(r"```", "", cleaned_text)

        # Extract JSON part
        json_match = re.search(r"(\{.*\})", cleaned_text, flags=re.DOTALL)
        if json_match:
            json_text = json_match.group(1).strip()
            
            try:
                # Load as JSON
                out = json.loads(json_text)

                # # Pretty print the JSON output
                # out = json.dumps(json_data, indent=4)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)

        # out = json.loads(output)
        student_formated_response = out["student_formated_response"]
        teacher_formated_response = out["teacher_formated_response"]

        return student_formated_response, teacher_formated_response



    