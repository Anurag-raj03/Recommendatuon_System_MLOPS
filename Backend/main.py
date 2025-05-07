
import os
import sys
import pandas as pd
import joblib
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dataset_path = os.path.join("Data_Versioning", "raw_data", "Sample_df.csv")
cosine_sim_path = os.path.join("artifacts", "anime_cosine.jbl")
DB_PATH = os.path.join("Database_connection","anime_dat.db")

anime_df = pd.read_csv(dataset_path)
cosine_sim = joblib.load(cosine_sim_path)

def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)

class Anime(BaseModel):
    ID: int
    Title: str
    English: str
    Type: str
    Premiered: str
    Producers: str
    Studios: str
    Source: str
    Genres: str
    Themes: str
    Demographics: str
    Rating: str
    Score: str
    Synopsis: str

def fetch_image_url(anime_id):
    url = f"https://myanimelist.net/anime/{anime_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            image_tag = soup.find("img", {"class": "ac"})
            if image_tag:
                return image_tag.get("data-src")
    except Exception as e:
        print(f"Image Fetch Error: {e}")
    return None

def recommend_anime(anime_name: str):
    anime_name = anime_name.lower().strip()
    lower_english_names = anime_df["English"].str.lower().str.strip()
    
    if anime_name not in lower_english_names.values:
        return {"error": "Anime not found in dataset."}

    anime_index = lower_english_names[lower_english_names == anime_name].index[0]
    similar_anime_indices = sorted(
        list(enumerate(cosine_sim[anime_index])), key=lambda x: x[1], reverse=True
    )[1:4]

    recommendations = []
    for idx, _ in similar_anime_indices:
        similar_anime = anime_df.iloc[idx]
        anime_id = similar_anime["ID"]
        anime_title = similar_anime["English"]
        anime_link = f"https://myanimelist.net/anime/{anime_id}"
        anime_image = fetch_image_url(anime_id)

        recommendations.append({
            "name": anime_title,
            "link": anime_link,
            "image": anime_image or "No Image Available"
        })

    return {"recommendations": recommendations}

def anime_name_checking(conn, English):
    cur = conn.cursor()
    cur.execute("SELECT id FROM anime WHERE English = ?", (English,))
    result = cur.fetchone()
    cur.close()
    return result is not None

def insert_new_anime_data(conn, anime_data):
    if anime_name_checking(conn, anime_data["English"]):
        return
    sql = """
        INSERT INTO anime (
            Title, English, Type, Premiered, Producers, Studios,
            Source, Genres, Themes, Demographics, Rating, Score, Synopsis
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    values = (
        anime_data["Title"], anime_data["English"], anime_data["Type"],
        anime_data["Premiered"], anime_data["Producers"], anime_data["Studios"],
        anime_data["Source"], anime_data["Genres"], anime_data["Themes"],
        anime_data["Demographics"], anime_data["Rating"], anime_data["Score"],
        anime_data["Synopsis"]
    )

    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    cur.close()

@app.get("/")
def root():
    return {"message": "Anime Recommendation API is Running!"}

@app.get("/get_anime_list")
async def get_anime_list():
    return anime_df[["English"]].dropna().drop_duplicates().to_dict(orient="records")

@app.post("/add_anime/")
async def add_anime(anime: Anime):
    anime_data = anime.dict()
    
    try:
        conn = get_connection(DB_PATH)
        insert_new_anime_data(conn, anime_data)
        conn.close()
    except Exception as e:
        return {"message": "Error adding anime to DB", "error": str(e)}

    airflow_trigger_url = "http://airflow:8080/api/v1/dags/anime_etl_pipeline/dagRuns"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(b"admin:admin").decode("utf-8")
    }
    payload = {"conf": anime_data}

    try:
        response = requests.post(airflow_trigger_url, json=payload, headers=headers)
        if response.status_code == 200:
            return {"message": "Anime Added & Airflow Pipeline Triggered!"}
        else:
            return {"message": "Anime Added but Airflow Trigger Failed", "error": response.text}
    except Exception as e:
        return {"message": "Anime Added but Airflow Trigger Failed", "error": str(e)}

@app.get("/recommend_anime/{anime_name}")
async def get_recommendations(anime_name: str):
    return recommend_anime(anime_name)
