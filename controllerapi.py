import os
import PyPDF2
import csv
import spacy
import nltk
from nltk.tokenize import sent_tokenize
import pdfplumber
from sentence_transformers import SentenceTransformer
from flair.data import Sentence
from flair.models import TextClassifier
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
import re
from  viewapi import output
class ResumeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def shortlist(self, keywords):
        resume_texts = self.model.get_resume_texts()

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(resume_texts)

        cosine_similarities = linear_kernel(tfidf_matrix, vectorizer.transform([" ".join(keywords)])).flatten()

        match_list = [file for index, file in enumerate(os.listdir(self.model.resume_folder))
                      if cosine_similarities[index] * 100 > 1.00]
        match_list = sorted(match_list)

        self.view.display_shortlist(match_list)
        return match_list

    def process_resume(self, match_list,resume_dir, job_description):
            model = SentenceTransformer('all-MiniLM-L6-v2')
            classifier = TextClassifier.load('en-sentiment')

            # Get sentiment
            sentence = Sentence(job_description)
            classifier.predict(sentence)
            sentiment = sentence.labels[0].value

            # Encode job description
            job_embedding = model.encode(job_description)

            # Process resumes
            resume_scores = {}
            for filename in os.listdir(resume_dir):
                if filename in match_list:
                    if filename.endswith('.pdf'):

                        file_path = os.path.join(resume_dir, filename)
                        full_text=''
                        with pdfplumber.open(file_path) as pdf:
                            for page in pdf.pages:
                                full_text += page.extract_text()

                        full_text = re.sub(r'\W', ' ', full_text)
                        full_text = re.sub(r'\s+', ' ', full_text)

                        sentences = sent_tokenize(full_text)

                        # Get sentiment of sentences
                        positive_sents = []
                        for sent in sentences:
                            sentence = Sentence(sent)
                            classifier.predict(sentence)
                            if sentence.labels[0].value == sentiment:
                                positive_sents.append(sent)

                        if len(positive_sents) > 0:
                                job_embedding = model.encode(job_description)
                                resume_embeddings = model.encode(positive_sents)
                                cosine_scores = cosine_similarity([job_embedding], resume_embeddings) # type: ignore
                                score = np.mean(np.max(cosine_scores, axis=1))
                        else:
                                score = 0

                        # print(f'{filename}: {score*100:.2f}% match')
                        resume_scores[filename] = score

            result=self.view.display_final_list(resume_scores)
            return result