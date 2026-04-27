from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database import engine, course_table


MINIMUM_SCORE = 0.12
MAX_RESULTS = 3


def clean_text(text):
   if text is None:
       return ""

   text = text.lower()
   text = text.replace(",", " ")
   text = text.replace(".", " ")
   text = text.strip()

   return text


def fetch_courses():
   with engine.connect() as connection:
       rows = connection.execute(course_table.select()).fetchall()

   courses = []

   for row in rows:
       courses.append({
           "name": row.course_name,
           "description": row.course_description,
           "keywords": row.course_keywords
       })

   return courses


def build_course_text(course):
   return f"{course['keywords']} {course['description']}"


def get_recommendations(user_input):
   user_query = clean_text(user_input)

   if user_query == "":
       return []

   all_courses = fetch_courses()

   if len(all_courses) == 0:
       return []

   course_documents = []

   for course in all_courses:
       course_documents.append(build_course_text(course))

   documents = course_documents + [user_query]

   vectorizer = TfidfVectorizer()
   tfidf_matrix = vectorizer.fit_transform(documents)

   user_vector = tfidf_matrix[-1]
   courses_vectors = tfidf_matrix[:-1]

   similarity_scores = cosine_similarity(user_vector, courses_vectors)[0]

   results = []

   for index, score in enumerate(similarity_scores):
       if score >= MINIMUM_SCORE:
           course = all_courses[index]

           results.append({
               "title": course["name"],
               "description": course["description"],
               "skills": course["keywords"],
               "score": round(float(score), 3)
           })

   results.sort(key=lambda item: item["score"], reverse=True)

   return results[:MAX_RESULTS]