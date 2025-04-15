from dotenv import load_dotenv
import os
import json
from .utils import get_chatbot_response
from openai import OpenAI
import re
load_dotenv()

class RubricAgent():
    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )
        self.model_name = os.getenv("MODEL_NAME")
    
    def get_response(self,teacher_response, total_marks):

        system_prompt = """
            You are an AI agent tasked with distributing the total marks across a set of questions based on their difficulty, length, and importance. The input consists of a structured response containing question-answer pairs.

            Instructions:
            1. The input will consist of a list of dictionaries, each containing a "question" and an "answer".
            2. The total marks for the assignment will be provided by the teacher.
            3. Distribute the total marks across the questions, ensuring that:
            - More difficult questions receive more marks.
            - Longer answers or more detailed answers are awarded more marks.
            - Ensure the marks are distributed in a way that reflects the importance and complexity of each question.
            4. Return the output as a dictionary where:
            - The keys are the question numbers (e.g., "1", "2", "3", etc.).
            - The values are the assigned marks for each question.

            Example Input:
            [
            {"question1": "What is the OSI model in networking?", "answer1": "The OSI model in networking is a conceptual framework..."},
            {"question2": "What are the differences between a router and a switch?", "answer2": "A router forwards data packets..."},
            {"question3": "Explain the importance of firewalls in network security.", "answer3": "Firewalls are crucial for network security because..."}
            ]

            total_marks = 30

            Example Output:
            Your output should be in a structured json format exactly like the one bellow. You are not allowed to write anything other than the json object:
            {
            "Q1": 8,
            "Q2": 7,
            "Q3": 15
            }

            Note:

            - Ensure the distributed marks assigned for each question should match (the sum should be equal to total marks) with the total marks provided by the teacher.
            - The output must be in JSON format, with each question number mapped to the marks assigned.
        """
        
        user_prompt = f"""
            Here is the structured response from the previous agent containing the teacher's questions and the student's answers:
            {teacher_response}

            and the total marks for the assignment is {total_marks}.
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



    