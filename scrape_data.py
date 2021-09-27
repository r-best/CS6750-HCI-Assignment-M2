from google_play_scraper import Sort, reviews
from pprint import pprint

revs, _ = reviews(
    'com.venmo',
    lang='en',
    country='us',
    sort=Sort.NEWEST,
    count=10
)

with open('data/reviews.csv', 'w', encoding='utf-8') as fp:
    fp.write("Stars|Comment\n")
    for x in revs:
        fp.write(f"{x['score']}|{x['content']}\n")
