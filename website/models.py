from flask import app, jsonify, redirect, request, url_for
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))  # You need a field for storing passwords
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    about = db.Column(db.Text)
    birthday = db.Column(db.Date)
    gender = db.Column(db.String(10))
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    linkedin = db.Column(db.String(150))
    # Define other fields as needed

    # Relationship with notes
    notes = db.relationship('Note', backref='user', lazy=True)
    # Relationship with experiences
    experiences = db.relationship('Experience', backref='user', lazy=True)
    # Relationship with educations
    educations = db.relationship('Education', backref='user', lazy=True)
    # Relationship with expertise
    expertises = db.relationship('Expertise', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Define other fields as needed

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150))
    position = db.Column(db.String(150))
    position_description = db.Column(db.Text)
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    currently_work_here = db.Column(db.Boolean, default=False)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Define other fields as needed

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(150))
    subject = db.Column(db.String(150))
    start = db.Column(db.Date)
    end = db.Column(db.Date)
    currently_study_here = db.Column(db.Boolean, default=False)
    degree = db.Column(db.String(100))
    certification = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Define other fields as needed

class Expertise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.Text)  # You can store skills as a comma-separated string or JSON
    area_of_expertise = db.Column(db.String(100))
    area_of_interest = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Define other fields as needed
  
