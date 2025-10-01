from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.model):
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.String(150), unique=True, nullable=False)
