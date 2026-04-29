from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text

DATABASE_URL = "sqlite:///Recommendation.db"

engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

course_table = Table(
   "courses",
   metadata,
   Column("id", Integer, primary_key=True),
   Column("course_name", String(150), nullable=False),
   Column("course_description", Text, nullable=False),
   Column("course_keywords", Text, nullable=False),
)

def setup_database():
   metadata.create_all(engine)