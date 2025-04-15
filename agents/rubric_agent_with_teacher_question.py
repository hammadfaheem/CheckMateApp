from dotenv import load_dotenv
import os
import json
from .utils import get_chatbot_response
from openai import OpenAI
import re
load_dotenv()

class RubricAgentTeacherQuestion():
    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")
    
    def get_response(self,questions):

        system_prompt = """
            You are an AI assistant that processes raw text containing a list of questions from a teacher.
            Your task is to extract the marks assigned to each question and return a structured JSON output.

            Instructions:
            1. Identify each question number in the provided text.
            2. Locate the marks assigned to each question. Marks are typically denoted by keywords such as "marks", "pts", or symbols like "/5", "[5]", etc.
            3. Return a JSON object where each key represents the question number, and the value is the marks assigned to that question.
            4. If a question does not explicitly mention marks, exclude it from the output.
            5. If the provided text does not contain any assigned marks for any questions, return an empty JSON object (i.e., {}).

            Examlpe Input:
            1. What is the OSI model in networking? marks 5
            2. What are the differences between a router and a switch? marks 5
            3. Explain the importance of firewalls in network security. marks 5

            Output Format:
            {
            "Q1": 5,
            "Q2": 5,
            "Q3": 5
            ...
            }

            (Where "Q1", "Q2", "Q3" are question numbers, and their respective values represent the marks assigned to them.)

            Ensure accuracy and consistency while extracting data. You are not allowed to return anything other than the JSON object and  and don't include this as well ```json```
            
            Note: 
                - donot return empty json object, marks are mentioned in questions
                - if you any one queestion then rubric should have only one question mark in the rubric.
            """

        
        user_prompt = f"""
            teacher's questions are
            {questions}
        """

        input_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
            ]

        output =get_chatbot_response(self.client,self.model_name,input_messages)
        output = self.postprocess(output)
        
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



    