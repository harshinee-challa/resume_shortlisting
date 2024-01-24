import os
import PyPDF2
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from flair.data import Sentence
from flair.models import TextClassifier
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
import re
import spacy
nlp = spacy.load("en_core_web_sm")
class ResumeModel:
    def __init__(self, resume_folder):
        self.resume_folder = resume_folder

    def extract_text_from_pdf(self, pdf_file):
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text

    def get_resume_texts(self):
        resume_texts = []
        for file in os.listdir(self.resume_folder):
            if file.endswith(".pdf"):
                file_path = os.path.join(self.resume_folder, file)
                text = self.extract_text_from_pdf(file_path)
                resume_texts.append(text)
        return resume_texts
    
    def extract_skills_nlp_based(self,job_description):
            # Load the spaCy English model
        nlp = spacy.load("en_core_web_sm")

        # Process the job description using spaCy
        doc = nlp(job_description)
        
        # Extract nouns as potential skills (assuming skills are often nouns)
        extracted_skills = [token.text for token in doc if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN')]

        return extracted_skills