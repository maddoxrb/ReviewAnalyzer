import pandas as pd
import matplotlib.pyplot as plt
from wordcloud_generator import WordCloud
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime
from collections import Counter
from IPython.display import Image, display

import json
import re

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

# Analyze rating distribution
plt.figure(figsize=(10, 5))
df['rating'].hist(bins=5, range=(0.5, 5.5), edgecolor='black')
plt.title('Sampled Rating Distribution')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.xticks([1, 2, 3, 4, 5])
plt.show()


# Sentiment Analysis using TextBlob
df['sentiment'] = df['body'].apply(lambda x: TextBlob(x).sentiment.polarity)
plt.figure(figsize=(10, 5))
df['sentiment'].hist(bins=50)
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Frequency')
plt.show()

# # Time Series Analysis
def extract_date(date_str):
    match = re.search(r'on ([A-Za-z]+\s\d{1,2},\s\d{4})', date_str)
    if match:
        return pd.to_datetime(match.group(1))
    return None

df['date'] = df['date'].apply(extract_date)

# Time Series Analysis
df.set_index('date', inplace=True)

# Resample by month and interpolate missing values
monthly_avg_rating = df['rating'].resample('M').mean().interpolate()

# Plot the interpolated time series
plt.figure(figsize=(10, 5))
monthly_avg_rating.plot()
plt.title('Average Rating Over Time')
plt.xlabel('Date')
plt.ylabel('Average Rating')
plt.show()

# Word Cloud
all_reviews = ' '.join(df['body'])
wordcloud = WordCloud(width=800, height=400, max_words=100).generate(all_reviews)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Reviews')
plt.show()

#Print most helpful review
def extract_helpful_count(helpful_str):
    match = re.search(r'(\d+)', helpful_str)
    return int(match.group(1)) if match else 0

df['helpful_count'] = df['helpful'].apply(extract_helpful_count)

# Find the review with the highest helpful count
most_helpful_review = df.loc[df['helpful_count'].idxmax()]

# Print the most helpful review
print("Most Helpful Review:")
print(f"Title: {most_helpful_review['title']}")
print(f"Rating: {most_helpful_review['rating']}")
print(f"Body: {most_helpful_review['body']}")
print(f"Helpful Count: {most_helpful_review['helpful_count']}")
print(f"Date: {most_helpful_review['date']}")
print(f"Author: {most_helpful_review['author_title']}")


#Extract reviews that contain image URLs
reviews_with_images = df[df['image_url'].apply(lambda x: len(x) > 0)]

# Gather a list of image URLs
image_urls = []
for images in reviews_with_images['image_url']:
    image_urls.extend(images)

# Limit to at most five image URLs
image_urls = image_urls[:5]

# Display the images
for url in image_urls:
    print(url)