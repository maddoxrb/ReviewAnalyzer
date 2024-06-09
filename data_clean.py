import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string

# # Download NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# Initialize the WordNet lemmatizer and set of stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_review(review):
    # Tokenize the review
    tokens = word_tokenize(review)
    # Remove punctuation
    tokens = [word for word in tokens if word.isalnum()]
    # Convert tokens to lowercase
    tokens = [word.lower() for word in tokens]
    # Remove stopwords and single character words
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    # Lemmatize tokens
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

def print_review_info(review):
    cleaned_title = clean_review(review.get('title', ''))
    cleaned_body = clean_review(review.get('body', ''))
    print(f"Review Title: {cleaned_title}")
    print(f"Author: {review.get('author_title')}")
    print(f"Date: {review.get('date')}")
    print(f"Rating: {review.get('rating_text')}")
    print(f"Helpful: {review.get('helpful')}")
    print(f"Review:\n{cleaned_body}\n")
    print("-" * 80)


# Example usage
review = "This is a sample review, with some punctuation! And stop words."
cleaned_review = clean_review(review)
print(cleaned_review)
