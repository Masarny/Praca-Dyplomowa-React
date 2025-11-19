from database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    passwords = db.relationship("StoredPassword", backref="owner", lazy=True)
    totp_secret = db.Column(db.String(32), nullable=True)


class StoredPassword(db.Model):
    __tablename__ = "passwords"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    site = db.Column(db.String(255), nullable=False)
    login = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
