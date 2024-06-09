import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import json
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Set Matplotlib backend to 'Agg'
plt.switch_backend('Agg')

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def generate_word_cloud():
    with open('biotin_reviews.json', 'r') as file:
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

    # Ensure the static directory exists
    os.makedirs('static', exist_ok=True)

    plt.style.use('seaborn-darkgrid')
    plt.rcParams.update({
        'axes.facecolor': '#2d2d2d',
        'axes.edgecolor': '#cbd5e0',
        'axes.labelcolor': '#cbd5e0',
        'xtick.color': '#cbd5e0',
        'ytick.color': '#cbd5e0',
        'text.color': '#cbd5e0',
        'figure.facecolor': '#1a1a1a',
        'figure.edgecolor': '#1a1a1a',
        'savefig.facecolor': '#1a1a1a',
        'savefig.edgecolor': '#1a1a1a',
        'grid.color': '#4a5568',
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans', 'Bitstream Vera Sans', 'sans-serif'],
        'font.size': 12,
        'axes.titlesize': 16
    })

    result_paths = {}

    # Generate Word Cloud
    try:
        all_reviews = ' '.join(df['body'].dropna())
        wordcloud = WordCloud(width=800, height=400, max_words=100, background_color='#2d2d2d', colormap='Blues').generate(all_reviews)
        wordcloud_path = 'static/wordcloud.png'
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(wordcloud_path, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        result_paths['wordcloud'] = wordcloud_path
    except Exception as e:
        print(f"Error generating word cloud: {e}")

    # Analyze rating distribution
    try:
        plt.figure(figsize=(10, 5))
        df['rating'].dropna().astype(int).hist(bins=5, range=(0.5, 5.5), edgecolor='black', color='#3182ce')
        plt.title('Sampled Rating Distribution', fontsize=16)
        plt.xlabel('Rating')
        plt.ylabel('Frequency')
        plt.xticks([1, 2, 3, 4, 5])
        rating_dist_path = 'static/rating_distribution.png'
        plt.savefig(rating_dist_path, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        result_paths['rating_distribution'] = rating_dist_path
    except Exception as e:
        print(f"Error generating rating distribution: {e}")

    # Sentiment Analysis using TextBlob
    try:
        df['sentiment'] = df['body'].dropna().apply(lambda x: TextBlob(x).sentiment.polarity)
        plt.figure(figsize=(10, 5))
        df['sentiment'].hist(bins=50, color='#63b3ed')
        plt.title('Sentiment Distribution', fontsize=16)
        plt.xlabel('Sentiment')
        plt.ylabel('Frequency')
        sentiment_dist_path = 'static/sentiment_distribution.png'
        plt.savefig(sentiment_dist_path, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        result_paths['sentiment_distribution'] = sentiment_dist_path
    except Exception as e:
        print(f"Error generating sentiment distribution: {e}")

    # Extract the date and location
    def extract_date_and_location(date_str):
        date_match = re.search(r'on ([A-Za-z]+\s\d{1,2},\s\d{4})', date_str)
        location_match = re.search(r'Reviewed in (.*?) on', date_str)
        date = pd.to_datetime(date_match.group(1)) if date_match else None
        location = location_match.group(1) if location_match else None
        return date, location

    try:
        df[['date', 'location']] = df['date'].apply(lambda x: pd.Series(extract_date_and_location(x)))

        # Set the date as the DataFrame index
        df.set_index('date', inplace=True)
        monthly_avg_rating = df['rating'].resample('M').mean().interpolate()

        plt.figure(figsize=(10, 5))
        monthly_avg_rating.plot(color='#63b3ed')
        plt.title('Average Rating Over Time', fontsize=16)
        plt.xlabel('Date')
        plt.ylabel('Average Rating')
        time_series_path = 'static/time_series.png'
        plt.savefig(time_series_path, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        result_paths['time_series'] = time_series_path
    except Exception as e:
        print(f"Error generating time series analysis: {e}")

    # Generate Horizontal Bar Chart for locations
    try:
        location_counts = df['location'].value_counts()
        plt.figure(figsize=(12, 6))
        location_counts.plot(kind='barh', color='#63b3ed')
        plt.title('Proportion of Reviewers by Location', fontsize=16)
        plt.xlabel('Number of Reviews')
        plt.ylabel('Location')
        plt.gca().invert_yaxis()
        location_bar_path = 'static/location_bar.png'
        plt.savefig(location_bar_path, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        result_paths['location_bar'] = location_bar_path
    except Exception as e:
        print(f"Error generating location bar chart: {e}")

    # Find the most helpful review
    def extract_helpful_count(helpful_str):
        match = re.search(r'(\d+)', helpful_str)
        return int(match.group(1)) if match else 0

    try:
        df['helpful_count'] = df['helpful'].apply(extract_helpful_count)
        most_helpful_review = df.loc[df['helpful_count'].idxmax()]

        most_helpful_review_text = {
            "title": most_helpful_review['title'],
            "rating": int(most_helpful_review['rating']),
            "body": most_helpful_review['body'],
            "helpful_count": int(most_helpful_review['helpful_count']),
            "author": most_helpful_review['author_title'],
            "location": most_helpful_review['location']
        }
        result_paths['most_helpful_review'] = most_helpful_review_text
    except Exception as e:
        print(f"Error finding the most helpful review: {e}")

    # Separate positive and negative reviews
    try:
        positive_reviews = df[df['rating'] >= 4]['body'].dropna()
        negative_reviews = df[df['rating'] <= 2]['body'].dropna()

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

        result_paths['most_positive_words'] = most_positive_words
        result_paths['most_negative_words'] = most_negative_words
    except Exception as e:
        print(f"Error analyzing positive and negative reviews: {e}")

    # Common words across all reviews
    try:
        all_words = []
        for review in df['body'].dropna():
            all_words.extend(clean_and_tokenize(review))

        all_word_counts = Counter(all_words)
        most_common_words = all_word_counts.most_common(10)

        result_paths['most_common_words'] = most_common_words
    except Exception as e:
        print(f"Error analyzing most common words: {e}")

    # Replace empty or None variation names with "Untitled"
    try:
        df['variation'] = df['variation'].fillna('Untitled')
        df['variation'] = df['variation'].replace('', 'Untitled')

        # Average rating for each variation
        variation_avg_rating = df.groupby('variation')['rating'].mean().sort_values()
        plt.figure(figsize=(12, 6))
        ax = variation_avg_rating.plot(kind='bar', color='#63b3ed')
        plt.title('Average Rating for Each Variation', fontsize=16)
        plt.xlabel('Variation')
        plt.ylabel('Average Rating')
        plt.xticks(rotation=35, ha='right', fontsize=10)

        # Ensure all variations display correctly
        for label in ax.get_xticklabels():
            label.set_ha('right')

        avg_rating_variation_path = 'static/avg_rating_variation.png'
        plt.savefig(avg_rating_variation_path, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        result_paths['avg_rating_variation'] = avg_rating_variation_path
    except Exception as e:
        print(f"Error generating average rating for each variation: {e}")

    # Generate JSON for review cards
    try:
        reviews_json = df.to_dict(orient='records')
        with open('static/reviews.json', 'w') as json_file:
            json.dump(reviews_json, json_file, indent=4)
        result_paths['reviews'] = 'static/reviews.json'
    except Exception as e:
        print(f"Error generating review cards JSON: {e}")

    # Return the paths to generated visualizations
    return result_paths

# Execute the function to generate the results
if __name__ == '__main__':
    results = generate_word_cloud('glass_protector_reviews.json')
    print(results)
