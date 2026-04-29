from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
)