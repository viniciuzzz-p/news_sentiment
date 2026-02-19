import json
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import time

load_dotenv()
API_KEY = os.getenv("API_KEY")
caminho_arquivo = 'data/raw/all_news.csv'

url = "https://gnews.io/api/v4/search"


def coletar_noticias(query, max_noticias, max_paginas = 10):


    todas_noticias = []

    for page in range(1, max_paginas + 1):
        params = {
            "q": query,
            "lang": "en",
            "max": 10,
            "page": page,
            "apikey": API_KEY
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("Erro:", response.status_code)
            print(response.text)
            break

        dados = response.json()
        artigos = dados.get("articles", [])

        if not artigos:
            print(f"Sem mais resultados para {query} na página {page}")
            break

        for artigo in artigos:
            todas_noticias.append({
                "title": artigo.get("title"),
                "content": artigo.get("content"),
                "description": artigo.get("description"),
                "publication date": artigo.get("publishedAt"),
                "id": artigo.get("id"),
                "url": artigo.get("url"),
                "tema": query
            })

        print(f"{query} - Página {page} coletada")

        time.sleep(1)  


    return pd.DataFrame(todas_noticias)



temas = ["world", "nation", "science", "health"]
todos_df = []

for tema in temas:
    df = coletar_noticias(tema, max_noticias= 10)
    todos_df.append(df)

df_novas = pd.concat(todos_df, ignore_index=True)

if os.path.exists(caminho_arquivo):
    df_antigo = pd.read_csv(caminho_arquivo)

    df_final = pd.concat([df_antigo, df_novas], ignore_index=True)
else:
    df_final = df_novas




df_final = df_final.reset_index(drop=True)

df_final.to_csv(caminho_arquivo, index=False)

print(f"Dataset atualizado! Total de notícias: {len(df_final)}")