from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from headers import app


db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"


class SavedJob(db.Model):
    __tablename__ = 'saved_job'
    id = db.Column(db.Integer, primary_key=True)
    # could make the username a foreign key, would need to change how SavedJob instances are created but this works fine for now
    username = db.Column(db.String(), nullable=False)
    job_id = db.Column(db.String())
    job_title=db.Column(db.String())
    company_name=db.Column(db.String())
    location=db.Column(db.String())
    description=db.Column(db.String())
    def __repr__(self):
        return f"Job:('{self.job_title}: {self.company_name}')"
# end Models