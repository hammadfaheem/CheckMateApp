# from sample_input import ai_text, human_text
# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import numpy as np
# import nltk
# from nltk.tokenize import sent_tokenize

# nltk.download('punkt')

# # Load GPT-2 Model and Tokenizer
# model_name = "gpt2"
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)
# model.eval()

# def calculate_perplexity(text):
#     """Compute perplexity of the given text using GPT-2"""
#     encodings = tokenizer(text, return_tensors="pt")
#     input_ids = encodings.input_ids
#     with torch.no_grad():
#         outputs = model(input_ids, labels=input_ids)
#         loss = outputs.loss
#     return torch.exp(loss).item()

# def calculate_burstiness(text):
#     """Compute burstiness as the standard deviation of sentence lengths"""
#     sentences = sent_tokenize(text)
#     sentence_lengths = [len(sentence.split()) for sentence in sentences]
#     return np.std(sentence_lengths)



# def classify_text(perplexity, burstiness, perplexity_threshold=22, burstiness_threshold=5.5):
#     """
#     Classifies text as 'AI' or 'Human' based on perplexity and burstiness.
    
#     Parameters:
#     - perplexity (float): Perplexity score from the language model
#     - burstiness (float): Standard deviation of sentence lengths
#     - perplexity_threshold (float): Threshold below which text is likely AI-generated
#     - burstiness_threshold (float): Threshold below which text is likely AI-generated
    
#     Returns:
#     - str: 'AI' or 'Human'
#     """
#     if perplexity < perplexity_threshold and burstiness < burstiness_threshold:
#         return "The text is likely to be generated by AI-generated"
#     else:
#         return "The text is likely to be Human-written"

# # Example Text
# text = """AI, or Artificial Intelligence, is when machines are designed to think and act like humans—at least in certain ways. It allows computers to learn from experience, recognize patterns, make decisions, and even understand language.

# There are different types of AI:

#     Narrow AI (also called Weak AI) is built for specific tasks, like voice assistants (Siri, Alexa), recommendation systems (Netflix, Spotify), or self-driving car technology.
#     General AI (Strong AI) is the idea of a machine that can think and learn just like a human across different areas—something that doesn’t exist yet.
#     Super AI is a futuristic concept where AI would surpass human intelligence entirely.

# AI works through technologies like machine learning (where computers learn from data), deep learning (a more advanced form of machine learning), and natural language processing (how AI understands and responds to human language). It’s used in everything from chatbots to medical diagnosis to self-driving cars."""

# perplexity = calculate_perplexity(text)
# burstiness = calculate_burstiness(text)


# # Compute Perplexity and Burstiness
# print("Text Perplexity:", perplexity)
# print("Text Burstiness:",  burstiness)


    
# classification = classify_text(perplexity, burstiness)
# print("Result: ", classification)



import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

class PlagiarismDetector:
    def __init__(self, model_name="gpt2", perplexity_threshold=22, burstiness_threshold=5.5):
        """
        Initializes the plagiarism detector with GPT-2 model and tokenizer.
        """
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        self.perplexity_threshold = perplexity_threshold
        self.burstiness_threshold = burstiness_threshold
    
    def calculate_perplexity(self, text):
        """Compute perplexity of the given text using GPT-2"""
        encodings = self.tokenizer(text, return_tensors="pt")
        input_ids = encodings.input_ids
        with torch.no_grad():
            outputs = self.model(input_ids, labels=input_ids)
            loss = outputs.loss
        return torch.exp(loss).item()
    
    def calculate_burstiness(self, text):
        """Compute burstiness as the standard deviation of sentence lengths"""
        sentences = sent_tokenize(text)
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        return np.std(sentence_lengths)
    
    def classify_text(self, text):
        """Classifies text as 'AI' or 'Human' based on perplexity and burstiness."""
        perplexity = self.calculate_perplexity(text)
        burstiness = self.calculate_burstiness(text)
        
        # print(f"Text Perplexity: {perplexity}")
        # print(f"Text Burstiness: {burstiness}")
        
        if perplexity < self.perplexity_threshold and burstiness < self.burstiness_threshold:
            result =  "The text is likely to be AI-generated"
        else:
            result =  "The text is likely to be Human-written"
        
        return result, perplexity, burstiness

# # Example Usage
# if __name__ == "__main__":
#     sample_text = """AI, or Artificial Intelligence, is when machines are designed to think and act like humans—at least in certain ways. 
#     It allows computers to learn from experience, recognize patterns, make decisions, and even understand language."""
    
#     detector = PlagiarismDetector()
#     result = detector.classify_text(sample_text)
#     print("Result:", result)
