from typing import List, Dict, Union
import string
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import logging
import json

nltk.download('stopwords')
nltk.download('wordnet')

logger = logging.getLogger()
stop_words = set(stopwords.words("english"))


def is_ascii(s: str) -> bool:
    """Check if a string `s` only contains ASCII characters."""
    return all(ord(c) < 128 for c in s)


class LSA:
    def __init__(self, vocab: Dict[str, int], documents: List[str], num_features: Union[int, float]):
        """
        Initialize the LSA (Latent Semantic Analysis) comparer.

        Args:
            vocab (Dict[str, int]): A dictionary mapping terms to indices.
            documents (List[str]): A list of documents used to fit the TF-IDF vectorizer.
            num_features (Union[int, float]): Number of features after dimension reduction.
                If `num_features` is a float, the number of reduced features will be
                `num_features * len(vocab)`.
        """
        logger.info('Initializing LSA comparer...')
        self.vocab = vocab
        self.documents = documents
        self.num_features = num_features if num_features > 1 else int(num_features * len(self.vocab))

        self.lemmatizer = WordNetLemmatizer()

        self.vectorizer = TfidfVectorizer(decode_error='replace', vocabulary=self.vocab)
        self.svd = TruncatedSVD(n_components=self.num_features, random_state=42)

    def preprocess_text(self, text: str) -> str:
        """Preprocess a given text."""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        words = [w for w in words if w not in stop_words and is_ascii(w) and not w.isdigit()]
        words = [self.lemmatizer.lemmatize(w) for w in words]
        words = [w if w in self.vocab else '_unknown_' for w in words]
        return ' '.join(words)

    def vectorize(self, document: str) -> np.ndarray:
        """Vectorize a document using TF-IDF and SVD."""
        preprocessed_doc = self.preprocess_text(document)
        tfidf_matrix = self.vectorizer.transform([preprocessed_doc])
        reduced_features = self.svd.transform(tfidf_matrix)
        return reduced_features

    def fit(self) -> None:
        """Preprocess all documents, fit the TF-IDF vectorizer, and fit the SVD model."""
        logger.info('Fitting vectorizer and feature reducer...')
        processed_docs = [self.preprocess_text(doc) for doc in self.documents]
        features_matrix = self.vectorizer.fit_transform(processed_docs)
        self.svd.fit(features_matrix)
        logger.info('LSA initialization complete.')

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def compare_two_text(self, text1: str, text2: str) -> float:
        """Compare two texts using LSA-based cosine similarity."""
        vec1 = self.vectorize(text1)
        vec2 = self.vectorize(text2)
        return self.cosine_similarity(vec1, vec2)


if __name__ == '__main__':
    texts = 'The cat sat on the mat with another cat sat on the floor and another cat sat on the table'
    vocab = make_vocab(texts, min_word_count=2)
    documents = ['The cat sat on the mat', 'Another cat sat on the floor', 'Yet another cat sat on the table']
    
    lsa = LSA(vocab, documents, num_features=50)
    lsa.fit()

    # Example usage: compare two texts
    similarity_score = lsa.compare_two_text('The cat on the mat', 'A cat is resting on a mat')
    print(f"Similarity score: {similarity_score}")
