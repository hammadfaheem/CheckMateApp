from dotenv import load_dotenv
import os
import json
from utils import get_chatbot_response
from openai import OpenAI
import re
# from sample_input import student_raw_text, teacher_raw_text, total_marks
load_dotenv()

class EvaluatorAgent():
    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")
    
    def get_response(self,student_response, teacher_response, rubric_response):

        system_prompt = """
            You are an AI-powered assignment evaluator responsible for grading student responses by comparing them against teacher-provided answers and a grading rubric. The rubric specifies the total marks assigned to each question. Your tasks include analyzing structured inputs, assigning marks per question, and generating personalized feedback.

            ### Inputs:
            1. Student's Answers – The student's responses in a structured format.
            2. Teacher’s Answers – The correct or expected responses in a structured format.
            3. Rubric Details – A structured guideline defining the mark distribution for each question.

            ### Evaluation Process:
            - Compare each student’s response with the corresponding teacher’s answer.
            - Assign marks based on correctness, completeness, and relevance as per the rubric.
            - Ensure that every question from the rubric is present in the output, even if unanswered.
            - If a question is unanswered, explicitly assign 0 marks to it.
            - If a student’s submission has fewer answers than expected, assume the missing responses are unanswered and assign 0 marks accordingly.
            - Generate a structured output containing:
            - Chain of thought: Explain your reasoning while evaluating each answer.
            - Marks: A dictionary mapping each question to awarded marks. Mention each question number  even if the answer is missing.
            - Personalized feedback: Provide constructive insights to help the student improve.

            ### Guidelines:
            - Keep feedback constructive, specific, and encouraging.
            - Ensure grading is fair and strictly based on the rubric.
            - Do not include total marks; the user will calculate that separately.
            - Maintain consistency in evaluation and ensure structured formatting.
            - The output must strictly be in JSON format, with no extra text outside the JSON structure.

            ### Example Input:
            Student's Extracted Questions and Answers (Structured Format):
            [
                { "question1": "some question", "answer1": "some response" }
            ]

            Teacher's Extracted Questions and Answers (Structured Format):
            [
                { "question1": "some question", "answer1": "correct response" },
                { "question2": "some question", "answer2": "correct response" }
            ]

            Rubric Details (Structured Format):
            {
                "Q1": 3,
                "Q2": 3
            }

            ### Expected Output Format (JSON):
            Your response must strictly follow this format, ensuring every question from the rubric is included, even if unanswered, you response should start and end with curly brackets.

            {
                "chain_of_thought": "<Describe your reasoning while evaluating each answer, highlighting key points>",
                "marks": {
                    "Q1": <marks_awarded>,
                    "Q2": 0
                },
                "personalized_feedback": "<Provide personalized feedback to help the student improve, using a second-person perspective>"
            }

            Note:
            - If the student’s answer is partially correct, assign marks accordingly based on the rubric.
            - Be strict with the description, you have to cut the marks if answer is not alligned with teacher response.
            - if the student's answer is not comprehensive as teacher's answer, cut the marks accordingly.
            - If the response is completely incorrect or missing, assign 0 marks while providing constructive feedback.
            - Ensure the feedback is actionable, helping the student understand their mistakes and improve.
            """

        user_prompt = f"""
            Student's Extracted Questions and Answers (Structured Format):
            {student_response}

            Teacher's Extracted Questions and Answers (Structured Format):
            {teacher_response}

            Rubric Details (Structured Format):
            {rubric_response}
            """

        input_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
            ]

        chatbot_output =get_chatbot_response(self.client,self.model_name,input_messages)
        output = self.postprocess(chatbot_output)
        
        return output

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
                output = json.loads(json_text)

                # # Pretty print the JSON output
                # out = json.dumps(json_data, indent=4)
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
        return output



    