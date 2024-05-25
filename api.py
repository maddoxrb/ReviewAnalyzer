from outscraper import ApiClient
import json

api_client = ApiClient(api_key='MTc3NzdlNWI5Y2M0NGRlOTg0YTcyODdhYjVhYzYxODV8ODg1Zjg2ZDY1Mw')
results = api_client.amazon_reviews(
    'https://www.amazon.com/Natures-Bounty-Supplement-Supports-10000mcg/dp/B009SZXM4E?_encoding=UTF8&fpw=new&fpl=fresh&ref_=eemb_mb_cat_hpc_m_d_sf_6_4_t&pf_rd_p=e60b658d-4c6a-4f63-ad69-760fef38b278&pf_rd_r=4AQA2XV9RBJ9Q4665CJW', 
    limit=3, 
    sort='recent'
)

# Print the structure of the results to understand it
print(json.dumps(results, indent=4))

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
