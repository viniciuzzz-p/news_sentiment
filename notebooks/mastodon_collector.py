import pandas as pd
from mastodon import Mastodon
import json
from bs4 import BeautifulSoup
import time

caminho_arquivo = 'data/raw/mastodon.csv'


mastodon = Mastodon( 
    api_base_url="https://mastodon.social"
)

posts = mastodon.timeline_hashtag("politics", limit=40)




def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

topics = [
    "politics",
    "technology",
    "climate",
    "health",
    "economy",
    "science",
    "sports"
]

all_data = []
seen_ids = set()

for topic in topics:
    print(f"coletando sobre #{topic}")
    topic_count = 0
    posts = mastodon.timeline_hashtag(topic, limit=40)

    while posts and topic_count < 200:
        for post in posts:
            if post["id"] in seen_ids:
                continue
            
            
            seen_ids.add(post["id"])

            all_data.append({
                "topic": topic,
                "text": clean_html(post["content"]),
                "created_at": post["created_at"],
                "likes": post["favourites_count"],
                "reblogs": post["reblogs_count"],
                "replies": post["replies_count"],
                "followers": post["account"]["followers_count"]
            })
            topic_count += 1

            if topic_count >=200:
                 break

        posts = mastodon.fetch_next(posts)
        time.sleep(1)

       

print("Total coletado:", len(all_data))

df = pd.DataFrame(all_data)


df = df[df["text"].str.len() > 20]
df = df.drop_duplicates(subset="text")


df.to_csv(caminho_arquivo, index= False)