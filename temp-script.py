import sqlalchemy as db
import pandas as pd
import pprint
import secrets
from job_search import db
from job_search import User
# print(User.query.all())
engine = db.create_engine('sqlite:///jobify.db', {})
query = engine.execute(f"SELECT * FROM User;").fetchall()
print(query)