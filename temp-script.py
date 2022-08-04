import sqlalchemy as db
import pandas as pd
from pprint import pprint
import secrets
from job_search import db
from job_search import User
# print(User.query.all())
engine = db.create_engine('sqlite:///jobify.db', {})
query = engine.execute(f"SELECT * FROM saved_job WHERE username='test4';").fetchall()
pprint(query)