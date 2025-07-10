from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

app = FastAPI()
BASE_DIR = "fastapi_recommendation"

class RecipeInput(BaseModel):
    name: str
    top_n: int = 3

class MoodInput(BaseModel):
    mood: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["http://localhost:3000"] for stricter policy
    allow_methods=["*"],
    allow_headers=["*"],
)

tf1 = joblib.load(os.path.join(BASE_DIR, "tfidf_comfort.pkl"))
tf2 = joblib.load(os.path.join(BASE_DIR, "tfidf_recipe.pkl"))

x = pd.read_csv(os.path.join(BASE_DIR, "x.csv"))
y = pd.read_csv(os.path.join(BASE_DIR, "y.csv"))
p = pd.read_csv(os.path.join(BASE_DIR, "p.csv"))
q = pd.read_csv(os.path.join(BASE_DIR, "q.csv"))

# Pydantic models for input validation
class RecipeInput(BaseModel):
    name: str
    top_n: int = 3

class MoodInput(BaseModel):
     mood: str
     top_n:int =3

@app.post("/recommend_recipe")
def recommend_recipe(data:RecipeInput):
    cleaned = data.name.lower().translate(str.maketrans("", "", string.punctuation))
    input_vect = tf2.transform([cleaned])
    simi = cosine_similarity(input_vect, tf2.transform(x["Name"])).flatten()
    index = simi.argsort()[::-1][:data.top_n]
    output_x = x.iloc[index]
    output_y = y.iloc[index]
    return {
        "results": [
            {
                "Name": row["Name"],
                "C_Type": row["C_Type"],
                "Veg_Non": row["Veg_Non"],
                "Ingredients": output_y.iloc[i]
            }
            for i, row in enumerate(output_x.to_dict(orient="records"))
        ]
    }

@app.post("/recommend_food")
def recommend_food(data:MoodInput):
    cleaned_input = data.mood.lower().translate(str.maketrans('', '', string.punctuation))
    input_vector = tf1.transform([cleaned_input])
    sim = cosine_similarity(input_vector, tf1.transform(p["comfort_food_reasons"]))
    best_index = sim.argmax()
    food = q.iloc[best_index]["comfort_food"]
    foods = [f.strip() for f in food.split(",")]
    return {"recommended_foods": foods}

@app.get('/healthcheck')
def checkStatus():
    return {"message":"working"}

