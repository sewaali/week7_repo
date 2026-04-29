import numpy as np
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommender.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS (Day 2) ---

# Many-to-Many Link Table for User <-> Skill
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    skills = db.relationship('Skill', secondary=user_skills, backref='users')

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    embedding = db.Column(db.PickleType) # Stores the 384-dimensional vector

# --- AI ENGINE INITIALIZATION (Day 1) ---

# Load the transformer model once at startup
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- RECOMMENDATION LOGIC ---

def get_recommendations(user_skill_names, all_courses):
    if not user_skill_names or not all_courses:
        return []

    # 1. Skill -> Embedding
    skill_embeddings = model.encode(user_skill_names)
    
    # 2. User Profile Vector (Average Pooling)
    user_vector = np.mean(skill_embeddings, axis=0).reshape(1, -1)

    # 3. Extract Course Vectors
    course_vectors = [c.embedding for c in all_courses]
    
    # 4. Semantic Matching (Cosine Similarity)
    scores = cosine_similarity(user_vector, course_vectors)[0]

    # 5. Ranking
    ranked_list = []
    for i, score in enumerate(scores):
        ranked_list.append({
            "title": all_courses[i].title,
            "description": all_courses[i].description,
            "score": round(float(score), 4)
        })
    
    return sorted(ranked_list, key=lambda x: x['score'], reverse=True)

# --- API ENDPOINTS ---

@app.route('/')
def home():
    return "<h1>AI Recommendation Engine</h1><p>Visit <b>/api/recommend/1</b></p>"

@app.get("/api/recommend/<int:user_id>")
def recommend_api(user_id):
    # Retrieve user and their skills from DB
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found. Run 'flask init-db' first."}), 404
    
    skill_names = [s.name for s in user.skills]
    all_courses = Course.query.all()
    
    # Run the pipeline
    recommendations = get_recommendations(skill_names, all_courses)
    
    return jsonify({
        "user_name": user.name,
        "skills": skill_names,
        "recommendations": recommendations[:3] # Top 3 matches
    })

# --- SETUP COMMAND ---

@app.cli.command("init-db")
def init_db():
    """Run 'flask init-db' to create database and sample data."""
    db.drop_all()
    db.create_all()
    
    # Create Skills
    s1 = Skill(name="Python")
    s2 = Skill(name="Deep Learning")
    s3 = Skill(name="React")
    
    # Create Courses with Embeddings (Day 1 Task)
    c1 = Course(title="Machine Learning 101", 
                description="Intro to AI and neural networks",
                embedding=model.encode("Machine Learning 101 Intro to AI and neural networks"))
    
    c2 = Course(title="Python for Data Science", 
                description="Pandas, Numpy, and data cleaning",
                embedding=model.encode("Python for Data Science Pandas, Numpy, and data cleaning"))
    
    c3 = Course(title="Frontend Mastery", 
                description="Building UI with modern JavaScript frameworks",
                embedding=model.encode("Frontend Mastery Building UI with modern JavaScript frameworks"))
    
    # Create User (Day 2 Task)
    user = User(id=1, name="Dev Student", skills=[s1, s2])
    
    db.session.add_all([s1, s2, s3, c1, c2, c3, user])
    db.session.commit()
    print("Database Initialized with User ID 1!")

if __name__ == '__main__':
    app.run(debug=True)