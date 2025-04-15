import PyPDF2
from .utils import read_pdf, process_llm, process_pdfs
from src.prompts import *
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import os
import zipfile
import pandas as pd
from groq import Groq
import json
import shutil
import time
from openai import OpenAI


class Grader:
    def __init__(self, answer_key_pdf, student_zip, total_marks, prompt, model, temperature):
        self.answer_key_pdf = answer_key_pdf
        self.student_zip = student_zip
        self.total_marks = total_marks
        self.prompt = prompt
        self.model = model
        self.temperature = temperature

        self.client = OpenAI(
            api_key=os.getenv("RUNPOD_TOKEN"),
            base_url=os.getenv("RUNPOD_CHATBOT_URL"),
        )

        self.model_name = os.getenv("MODEL_NAME")


    def read_pdf_pages(file_path):
        reader = PyPDF2.PdfReader(file_path)
        num_pages = len(reader.pages)
        content = ""
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            text = text.replace("\n", " ")
            text = "\n".join(["Question" + paragraph for paragraph in text.split("Question")])
            content += text
        return content
    