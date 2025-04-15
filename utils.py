
def get_chatbot_response(client,model_name,messages,temperature=0):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=temperature,
        top_p=0.8,
        max_tokens=2000,
    ).choices[0].message.content
    
    return response


def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chatbot_response(client,model_name,messages)

    return response



import os
from PyPDF2 import PdfReader
import docx  # Make sure to install python-docx (pip install python-docx)

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        reader = PdfReader(file_path)
        # Extract text from each page and join them with newline characters
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.split("\n")
    
    elif ext in ['.doc', '.docx']:
        # Read the DOC/DOCX file using python-docx
        document = docx.Document(file_path)
        full_text = [para.text for para in document.paragraphs]
        return full_text

    elif ext == '.txt':
        # Open and read the TXT file
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    
    else:
        raise ValueError(f"Unsupported file extension: {ext}")