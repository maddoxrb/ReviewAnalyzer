from outscraper import ApiClient
import json

api_client = ApiClient(api_key='MTc3NzdlNWI5Y2M0NGRlOTg0YTcyODdhYjVhYzYxODV8ODg1Zjg2ZDY1Mw')
results = api_client.amazon_reviews(
    'https://www.amazon.com/ebossy-Womens-Through-Embroidery-Distressed/product-reviews/B088JZTJQB/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews', 
    limit=50, 
    sort='recent'
)

# Print the structure of the results to understand it
print(json.dumps(results, indent=4))

# Save the results to a file
with open('jacket_reviews.json', 'w') as f:
    json.dump(results, f, indent=4)

# Extract the reviews data assuming the structure is known from the example
if results and isinstance(results, list) and len(results) > 0:
    reviews = results[0]
else:
    reviews = []

# Function to print each review in a nice format
def print_review(review):
    print(f"Review Title: {review.get('title')}")
    print(f"Author: {review.get('author_title')}")
    print(f"Date: {review.get('date')}")
    print(f"Rating: {review.get('rating_text')}")
    print(f"Helpful: {review.get('helpful')}")
    print(f"Review:\n{review.get('body')}\n")
    print("-" * 80)

# Print each review
for review in reviews:
    print_review(review)
