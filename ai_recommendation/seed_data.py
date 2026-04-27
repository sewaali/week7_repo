from database import engine, course_table, setup_database

setup_database()

courses_data = [
   {
       "course_name": "Artificial Intelligence Basics",
       "course_description": "This course introduces artificial intelligence, machine learning, neural networks, and smart systems.",
       "course_keywords": "ai artificial intelligence machine learning neural networks"
   },
   {
       "course_name": "Python Backend Development",
       "course_description": "Learn how to build backend applications using Python, Flask, APIs, routes, and databases.",
       "course_keywords": "backend python flask api database"
   },
   {
       "course_name": "Database Design and SQL",
       "course_description": "Learn database concepts, SQL queries, tables, relationships, and database design.",
       "course_keywords": "database sql tables relationships queries"
   },
   {
       "course_name": "Data Analysis Using Python",
       "course_description": "Learn data cleaning, pandas, charts, analysis, and working with datasets.",
       "course_keywords": "data analysis python pandas charts datasets"
   },
   {
       "course_name": "Frontend Web Development",
       "course_description": "Learn HTML, CSS, JavaScript, and how to build web pages.",
       "course_keywords": "html css javascript frontend web"
   },
   {
       "course_name": "Machine Learning Introduction",
       "course_description": "Learn supervised learning, unsupervised learning, models, training, and prediction.",
       "course_keywords": "machine learning ai models prediction training"
   },
   {
       "course_name": "Cyber Security Fundamentals",
       "course_description": "Learn cyber security basics, threats, attacks, protection, encryption, and network security.",
       "course_keywords": "cyber security cybersecurity threats attacks encryption protection"
   },
   {
       "course_name": "Ethical Hacking Introduction",
       "course_description": "Learn ethical hacking, penetration testing, vulnerabilities, and security tools.",
       "course_keywords": "ethical hacking penetration testing vulnerabilities security"
   },
   {
       "course_name": "Network Security Basics",
       "course_description": "Learn firewalls, secure networks, protocols, attacks detection, and network protection.",
       "course_keywords": "network security firewall protocols protection cyber"
   },
]

with engine.connect() as connection:
   connection.execute(course_table.delete())
   connection.execute(course_table.insert(), courses_data)
   connection.commit()

print("Courses inserted successfully.")