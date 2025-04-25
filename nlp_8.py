import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
from textblob import TextBlob
import string


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

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

def clean_text(text):
 
    text = re.sub(f'[{string.punctuation}]', '', text)

    text = re.sub(r'\d+', '', text)

    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_text(text):
    return word_tokenize(text)

def remove_stop_words(tokens):
    stop_words = set(stopwords.words('english'))
    return [token for token in tokens if token not in stop_words]

def correct_spelling(tokens):
    corrected_tokens = []
    for token in tokens:
        corrected = str(TextBlob(token).correct())
        corrected_tokens.append(corrected)
    return corrected_tokens

def stem_and_lemmatize(tokens):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stemmed = [stemmer.stem(token) for token in tokens]
    lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return stemmed, lemmatized

def create_trigrams(lemmatized_tokens):
    trigrams = []
    for i in range(len(lemmatized_tokens) - 2):
        trigram = lemmatized_tokens[i:i+3]
        trigrams.append(trigram)
    return trigrams

def tag_pos(lemmatized_tokens):
    return pos_tag(lemmatized_tokens)

def main():
    file_path = 'sample.txt'
    text = read_text_file(file_path)
    
    if text is None:
        return

    print("Original Text (first 200 chars):")
    print(text[:200] + "...\n")

    # 1. Text cleaning
    cleaned_text = clean_text(text)
    print("Cleaned Text (first 200 chars):")
    print(cleaned_text[:200] + "...\n")

    # 2. Convert to lowercase
    lower_text = cleaned_text.lower()
    print("Lowercase Text (first 200 chars):")
    print(lower_text[:200] + "...\n")

    # 3. Tokenization
    tokens = tokenize_text(lower_text)
    print("First 10 Tokens:")
    print(tokens[:10], "\n")

    # 4. Remove stop words
    filtered_tokens = remove_stop_words(tokens)
    print("First 10 Tokens after Stop Words Removal:")
    print(filtered_tokens[:10], "\n")

    # 5. Correct misspelled words
    corrected_tokens = correct_spelling(filtered_tokens)
    print("First 10 Tokens after Spelling Correction:")
    print(corrected_tokens[:10], "\n")

    # 6. Stemming and Lemmatization
    stemmed_tokens, lemmatized_tokens = stem_and_lemmatize(corrected_tokens)
    print("First 10 Stemmed Tokens:")
    print(stemmed_tokens[:10], "\n")
    print("First 10 Lemmatized Tokens:")
    print(lemmatized_tokens[:10], "\n")

    # 7. Create trigrams
    trigrams = create_trigrams(lemmatized_tokens)
    print("First 5 Trigrams:")
    print(trigrams[:5], "\n")

    # 8. POS Tagging
    pos_tags = tag_pos(lemmatized_tokens)
    print("First 10 POS Tags:")
    print(pos_tags[:10])

if __name__ == "__main__":
    main()