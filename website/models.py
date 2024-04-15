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

def add_experience():
    experience_data = request.json
    new_experience = Experience(
        company=experience_data['company'],
        position=experience_data['position'],
        position_description=experience_data['positionDesc'],
        start=experience_data['start'],
        end=experience_data['end'],
        currently_work_here=experience_data['currentlyWorkHere'],
        country=experience_data['country'],
        city=experience_data['city'],
        user_id=experience_data['user_id']
    )
    db.session.add(new_experience)
    db.session.commit()
    return jsonify({'message': 'Experience data added successfully'})

def add_education():
    education_data = request.json
    new_education = Education(
        organization=education_data['organization'],
        subject=education_data['subject'],
        start=education_data['start'],
        end=education_data['end'],
        currently_study_here=education_data['currentlyStudyHere'],
        degree=education_data['degree'],
        certification=education_data['certification'],
        user_id=education_data['user_id']
    )
    db.session.add(new_education)
    db.session.commit()
    return jsonify({'message': 'Education data added successfully'})

def add_skill():
    skill_data = request.json
    new_skill = Skill(
        skills=skill_data['skills'],
        user_id=skill_data['user_id']
    )
    db.session.add(new_skill)
    db.session.commit()
    return jsonify({'message': 'Skill data added successfully'})

def save_profile():
    # Extract profile data from the request
    profile_data = request.json

     # Get the user ID from the profile data
    user_id = profile_data.get('user_id')

        # Query the user record from the database based on the user ID
    user = User.query.get(user_id)

    if not user:
            # Return an error response if the user does not exist
         return jsonify({'message': 'User not found'}), 404

        # Update the user record with the profile data
    user.first_name = profile_data.get('first_name')
    user.last_name = profile_data.get('last_name')
    user.about = profile_data.get('about')
    user.birthday = profile_data.get('birthday')
    user.gender = profile_data.get('gender')
    user.country = profile_data.get('country')
    user.city = profile_data.get('city')
    user.linkedin = profile_data.get('linkedin')

        # Commit the changes to the database
    db.session.commit()
        
    return jsonify({'message': 'Profile data saved successfully'}), 200
    
  

