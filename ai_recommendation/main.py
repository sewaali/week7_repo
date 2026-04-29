from fastapi import FastAPI
from recommender import get_recommendations

app = FastAPI()


def extract_skills(user_text: str):
    return user_text.lower().split()


@app.get("/")
def home():
    return {"message": "AI Course Recommendation API is running 🚀"}


@app.get("/api/recommend")
def recommend(user_text: str):

    skills = extract_skills(user_text)

    if not skills:
        return {"error": "No skills detected"}

    results = get_recommendations(user_text)

    if not results:
        return {
            "message": "No strong matches found",
            "fallback": ["Python Basics", "Intro to Programming"]
        }

    return {
        "input": user_text,
        "skills": skills,
        "recommendations": results
    }