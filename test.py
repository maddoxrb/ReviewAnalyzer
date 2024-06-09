from data_clean import print_review_info


# def print_review_info(review):
#     print(f"Review Title: {review.get('title')}")
#     print(f"Author: {review.get('author_title')}")
#     print(f"Date: {review.get('date')}")
#     print(f"Rating: {review.get('rating_text')}")
#     print(f"Helpful: {review.get('helpful')}")
#     print(f"Review:\n{review.get('body')}\n")
#     print("-" * 80)



import json

# Load the JSON data from file
with open('jacket_reviews.json', 'r') as file:
    api_results = json.load(file)

# Check if 'reviews' key exists
reviews = api_results if isinstance(api_results, list) else api_results.get('reviews', [])

for review in reviews:
    if isinstance(review, list):
        for item in review:
            print_review_info(item)
    else:
        print_review_info(review)