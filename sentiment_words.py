import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from textblob import TextBlob
import pandas as pd
import json

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load the JSON data from file
with open('jacket_reviews.json', 'r') as file:
    api_results = json.load(file)

# Flatten the JSON data
reviews = []
for review in api_results:
    if isinstance(review, list):
        for item in review:
            reviews.append(item)
    else:
        reviews.append(review)

# Convert reviews to DataFrame for easier analysis
df = pd.json_normalize(reviews)

# Extract the rating from 'rating_text' if 'rating' field does not exist
if 'rating' not in df.columns and 'rating_text' in df.columns:
    df['rating'] = df['rating_text'].str.extract(r'(\d)').astype(int)

# Separate positive and negative reviews
positive_reviews = df[df['rating'] >= 4]['body']
negative_reviews = df[df['rating'] <= 2]['body']

# Function to clean and tokenize text
def clean_and_tokenize(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

# Initialize stopwords
stop_words = set(stopwords.words('english'))

# Tokenize and count word frequencies in positive reviews
positive_words = []
for review in positive_reviews:
    positive_words.extend(clean_and_tokenize(review))

positive_word_counts = Counter(positive_words)

# Tokenize and count word frequencies in negative reviews
negative_words = []
for review in negative_reviews:
    negative_words.extend(clean_and_tokenize(review))

negative_word_counts = Counter(negative_words)

# Perform sentiment analysis on the words
def word_sentiment(word):
    return TextBlob(word).sentiment.polarity

# Analyze the sentiment of the most common words
positive_word_sentiments = {word: word_sentiment(word) for word, count in positive_word_counts.most_common(100)}
negative_word_sentiments = {word: word_sentiment(word) for word, count in negative_word_counts.most_common(100)}

# Sort words by their sentiment scores
sorted_positive_words = sorted(positive_word_sentiments.items(), key=lambda item: item[1], reverse=True)
sorted_negative_words = sorted(negative_word_sentiments.items(), key=lambda item: item[1])

# Get the most positive and most negative words
most_positive_words = sorted_positive_words[:10]
most_negative_words = sorted_negative_words[:10]


print("Most Positive Words in Positive Reviews:")
for word, score in most_positive_words:
    print(f"{word}: {score}")

print("\nMost Negative Words in Negative Reviews:")
for word, score in most_negative_words:
    print(f"{word}: {score}")


