from flask import Flask, render_template, request
from database import setup_database
from recommendation_engine import get_recommendations

app = Flask(__name__)

setup_database()


@app.route("/", methods=["GET", "POST"])
def index():
   results = []
   searched = False

   if request.method == "POST":
       searched = True
       user_text = request.form.get("user_skills")
       results = get_recommendations(user_text)

   return render_template(
       "index.html",
       results=results,
       searched=searched
   )


if __name__ == "__main__":
   app.run(debug=True)