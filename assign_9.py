import re
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
import string
import pandas as pd

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def preprocess_text(text):
    text = re.sub(f'[{string.punctuation}]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens), tokens

def one_hot_encoding(documents, tokens_list):
    vocabulary = sorted(set(word for tokens in tokens_list for word in tokens))
    print(f"Vocabulary Size: {len(vocabulary)}")
    print(f"Sample Vocabulary (first 10): {vocabulary[:10]}\n")
    one_hot_matrices = []
    for tokens in tokens_list:
        matrix = np.zeros((len(tokens), len(vocabulary)), dtype=int)
        for i, token in enumerate(tokens):
            if token in vocabulary:
                matrix[i, vocabulary.index(token)] = 1
        one_hot_matrices.append(matrix)
    return one_hot_matrices, vocabulary

def main():
    file_paths = ['ml_concepts.txt', 'ml_applications.txt', 'ml_challenges.txt']
    documents = []
    tokens_list = []
    print("Step 1: Reading and Preprocessing Texts\n")
    for file_path in file_paths:
        text = read_text_file(file_path)
        if text is None:
            return
        print(f"Original Text ({file_path}, first 200 chars):")
        print(text[:200] + "...\n")
        processed_text, tokens = preprocess_text(text)
        documents.append(processed_text)
        tokens_list.append(tokens)
        print(f"Processed Text ({file_path}, first 100 chars):")
        print(processed_text[:100] + "...\n")
        print(f"Tokens ({file_path}, first 10):")
        print(tokens[:10], "\n")
    print("Step 2: One-Hot Encoding\n")
    one_hot_matrices, vocabulary = one_hot_encoding(documents, tokens_list)
    for i, matrix in enumerate(one_hot_matrices):
        print(f"One-Hot Matrix for {file_paths[i]} (shape: {matrix.shape}):")
        df = pd.DataFrame(matrix[:5], columns=vocabulary)
        print(df.iloc[:, :10], "\n")
    print("Step 3: Bag of Words\n")
    vectorizer = CountVectorizer()
    bow_matrix = vectorizer.fit_transform(documents)
    bow_feature_names = vectorizer.get_feature_names_out()
    print(f"BoW Vocabulary Size: {len(bow_feature_names)}")
    print(f"Sample BoW Vocabulary (first 10): {bow_feature_names[:10]}\n")
    print("BoW Matrix (dense, first 5 features):")
    print(pd.DataFrame(bow_matrix.toarray(), columns=bow_feature_names).iloc[:, :5], "\n")
    print("Step 4: TF-IDF\n")
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
    print(f"TF-IDF Vocabulary Size: {len(tfidf_feature_names)}")
    print(f"Sample TF-IDF Vocabulary (first 10): {tfidf_feature_names[:10]}\n")
    print("TF-IDF Matrix (dense, first 5 features):")
    print(pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_feature_names).iloc[:, :5], "\n")

if __name__ == "__main__":
    main()