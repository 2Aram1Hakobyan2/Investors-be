from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Education, Experience, Expertise, Note, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/user-profile')
@login_required
def user_profile():
    return render_template("user/yanifinal.html", user=current_user)

from datetime import datetime

@views.route('/startup-profile')
@login_required
def startup_profile():
    return render_template("user/startup profile.html", user=current_user)

@views.route('/investor-profile')
@login_required
def investor_profile():
    return render_template("user/profile.html", user=current_user)

@views.route('/add-experience', methods=['POST'])
@login_required
def add_experience():
    experience_data = request.json
    print('user_id', current_user.id)

    # Convert string dates to Python date objects
    start_date = datetime.strptime(experience_data['start'], '%Y-%m-%d')
    end_date = datetime.strptime(experience_data['end'], '%Y-%m-%d') if experience_data['end'] else None

    new_experience = Experience(
        company=experience_data['company'],
        position=experience_data['position'],
        position_description=experience_data['positionDesc'],
        start=start_date,
        end=end_date,
        currently_work_here=experience_data['currentlyWorkHere'],
        country=experience_data['country'],
        city=experience_data['city'],
        user_id=current_user.id
    )
    db.session.add(new_experience)
    db.session.commit()
    return jsonify({'message': 'Experience data added successfully'})

@views.route('/add-education', methods=['POST'])
@login_required
def add_education():
    education_data = request.json

    start_date = datetime.strptime(education_data['start'], '%Y-%m-%d')
    end_date = datetime.strptime(education_data['end'], '%Y-%m-%d') if education_data['end'] else None

    new_education = Education(
        organization=education_data['organization'],
        subject=education_data['subject'],
        start=start_date,
        end=end_date,
        currently_study_here=education_data['currentlyStudyHere'],
        degree=education_data['degree'],
        certification=education_data['certification'],
        user_id=current_user.id
    )
    db.session.add(new_education)
    db.session.commit()
    return jsonify({'message': 'Education data added successfully'})

@views.route('/add-skill', methods=['POST'])
@login_required
def add_expertise():
    skill_data = request.json
    new_skill = Expertise(
        skills=skill_data['skills'],
        user_id=current_user.id
    )
    db.session.add(new_skill)
    db.session.commit()
    return jsonify({'message': 'Skill data added successfully'})

@views.route('/save-profile', methods=['POST'])
@login_required
def save_profile():
    # Extract profile data from the request
    profile_data = request.json

     # Get the user ID from the profile data
    user_id = current_user.id

        # Query the user record from the database based on the user ID
    user = User.query.get(user_id)

    if not user:
            # Return an error response if the user does not exist
         return jsonify({'message': 'User not found'}), 404

        # Update the user record with the profile data
    user.first_name = profile_data.get('first_name')
    user.last_name = profile_data.get('last_name')
    user.about = profile_data.get('about')
    user.birthday = datetime.strptime(profile_data.get('birthday'), '%Y-%m-%d')
    user.gender = profile_data.get('gender')
    user.country = profile_data.get('country')
    user.city = profile_data.get('city')
    user.linkedin = profile_data.get('linkedin')

        # Commit the changes to the database
    db.session.commit()
        
    return jsonify({'message': 'Profile data saved successfully'}), 200
    