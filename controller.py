
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
import io
import spacy
nlp = spacy.load("en_core_web_sm")

class ResumeController:
    def __init__(self, view,database):
        self.database = database
        self.view = view
        self.job_description=""
        
    def extract_skills_nlp_based(self,jd):
            # Load the spaCy English model
        nlp = spacy.load("en_core_web_sm")
        #Input fofr Job Description
        self.job_description=jd
        
        # Process the job description using spaCy
        doc = nlp(self.job_description)
        
        # Extract nouns as potential skills (assuming skills are often nouns)
        extracted_skills = [token.text for token in doc if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN')]

        return extracted_skills

    def shortlist(self, keywords):
        resume_texts = self.database.get_pdf_text()

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(resume_texts)

        cosine_similarities = linear_kernel(tfidf_matrix, vectorizer.transform([" ".join(keywords)])).flatten()

        # match_list = [file for index, file in enumerate(os.listdir(self.database.get_filenames_from_azure()))
        #               if cosine_similarities[index] * 100 > 1.00]
        match_list = [filename for filename, similarity in zip(self.database.get_filenames_from_azure(), cosine_similarities)
                      if similarity * 100 >= 0]
        match_list = sorted(match_list)

        self.view.display_shortlist(match_list)
        return match_list

    def process_resume(self, match_list):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        classifier = TextClassifier.load('en-sentiment')

        sentence = Sentence(self.job_description)
        classifier.predict(sentence)
        sentiment = sentence.labels[0].value

        resume_scores = {}

        for filename in match_list:
                file_path = f"{self.database.container_name}/{filename}"
                with pdfplumber.open(self.database.download_blob(file_path)) as pdf:
                    full_text = ''
                    for page in pdf.pages:
                        full_text += page.extract_text()

                    full_text = re.sub(r'\W', ' ', full_text)
                    full_text = re.sub(r'\s+', ' ', full_text)

                    sentences = sent_tokenize(full_text)

                    positive_sents = []
                    for sent in sentences:
                        sentence = Sentence(sent)
                        classifier.predict(sentence)
                        if sentence.labels[0].value == sentiment:
                            positive_sents.append(sent)

                    if len(positive_sents) >0:
                        job_embedding = model.encode(self.job_description)
                        resume_embeddings = model.encode(positive_sents)
                        cosine_scores = cosine_similarity([job_embedding], resume_embeddings) #type:ignore
                        score = np.mean(np.max(cosine_scores, axis=1))
                    else:
                        score = 0

                    resume_scores[filename] = {
                        'filename': filename,
                        'score': score*100
                    }

        self.view.secondlist(resume_scores)
        return resume_scores


