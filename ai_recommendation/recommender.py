import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the model once
# This model converts text into 384-dimensional vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Converts a string into a numerical vector."""
    if not text:
        return None
    return model.encode(text)

def generate_recommendations(user_skills, course_objects, top_k=3):
    """
    Core logic:
    1. Average user skills into one 'interest vector'
    2. Compare interest vector to all course vectors
    3. Return ranked results
    """
    if not user_skills or not course_objects:
        return []

    # 1. Create the User Profile Vector (The 'Average' of their skills)
    skill_embeddings = model.encode(user_skills)
    # axis=0 averages across the columns to keep the 384 dimensions
    user_vector = np.mean(skill_embeddings, axis=0).reshape(1, -1)

    # 2. Extract pre-computed embeddings from your Course objects
    course_embeddings = [c.embedding for c in course_objects]
    
    # 3. Calculate Cosine Similarity
    # This returns an array of scores between 0 and 1
    similarity_scores = cosine_similarity(user_vector, course_embeddings)[0]

    # 4. Build the results list
    ranked_results = []
    for i, score in enumerate(similarity_scores):
        ranked_results.append({
            "course_id": course_objects[i].id,
            "title": course_objects[i].title,
            "score": round(float(score), 4),
            "description": course_objects[i].description
        })
    
    # 5. Sort by highest similarity score
    ranked_results.sort(key=lambda x: x['score'], reverse=True)
    
    return ranked_results[:top_k]