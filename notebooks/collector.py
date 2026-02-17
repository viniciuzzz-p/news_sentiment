import json
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "https://gnews.io/api/v4/search"

params = {
    "q": "world",
    "lang": "en",
    "max": 1,
    "apikey": API_KEY
}

response = requests.get(url, params=params)

dados = response.json()

noticias = []

for artigo in dados.get('articles', []):
    title = artigo.get('title', 'Title not available')
    content = artigo.get('content', 'Content not available')
    description = artigo.get('description', 'Description not available')
    pub_date = artigo.get('publishedAt', 'Date not available')
    id = artigo.get('id', 'N/A')

    artigo_info = {
        'title': title,
        'content': content,
        'description': description,
        'publication date': pub_date,
        'id': id
        
    }

    noticias.append(artigo_info)


df = pd.DataFrame(noticias)

df.to_csv('request.csv', index= False)
