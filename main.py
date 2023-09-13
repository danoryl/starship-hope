from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages, current_app, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileAllowed
import os
import re
from adventurelib import _handle_command
from functions import state
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dbmodels import *



app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db.init_app(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username field is required"),
        Length(min=2, message="Username must be at least 2 characters long")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password field is required"),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(
            regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
            message="Password must contain at least one letter, one number, and one special character (@$!%*?&)"
        )
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
          DataRequired(message="Confirm field is required"),
          EqualTo('password', message="Passwords must match")
    ])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username field is required")])
    password = PasswordField('Password', validators=[DataRequired(message="Password field is required")])
    
  
class ProfilePictureForm(FlaskForm):
    profile_picture = FileField('Profile Picture', validators=[
        DataRequired(message="Please select a file"),
        FileAllowed(['jpg', 'png', 'jpeg'])
    ])
    

class ChangeUsernameForm(FlaskForm):
    new_username = StringField('New Username', validators=[
        DataRequired(message="Username field is required"),
        Length(min=2, message="Username must be at least 2 characters long")
    ])
    

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(message="Current password field is required")])
    new_password = PasswordField('Password', validators=[
        DataRequired(message="New password field is required"),
        Length(min=8, message="Password must be at least 8 characters long"),
        Regexp(
            regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
            message="Password must contain at least one letter, one number, and one special character (@$!%*?&)"
        )
    ])
    confirm_new_password = PasswordField('Confirm Password', validators=[
          DataRequired(message="Confirm password field is required"),
          EqualTo('new_password', message="Passwords must match")
    ])
    

class DeleteUserForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(message="Password field is required")])
    

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
  
  
@app.before_first_request
def initialize_db():
    # Create the database tables first time the system is loaded if not present
    db.create_all()
    
    
    
@app.route('/')
def index():
    user_logged_in = current_user.is_authenticated    
    return render_template('index.html', user_logged_in=user_logged_in)


@app.route('/game')
@login_required
def game():
     
    return render_template('game.html')


@app.route('/input', methods=['POST'])
@login_required
@csrf.exempt
def handle_input():
    user_input = request.form['user_input']
    _handle_command(user_input)
    game_data = current_user.get_game_data()
    return game_data['gui']

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"success": False, "message": "Username already taken. Please choose a different username."})
                     
        hashed_password = generate_password_hash(password)  # Hash the password
        new_user = User(username=username, password=hashed_password)
        new_user.game_data = state  # Initialize session data for the new user
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return jsonify({"success": True, "message": "Registration success", "redirect": "/game"})
    else:
        # Form validation failed, return error messages
        errors = [msg for field_errors in form.errors.values() for msg in field_errors]
        return jsonify({"success": False, "message": errors})
        
  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = LoginForm() 
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return jsonify({"success": True, "message": "Login success", "redirect": "/game"})
            else:
                return jsonify({"success": False, "message": "Invalid credentials"})
        else:
            # Form validation failed, return error messages
            errors = [msg for field_errors in login_form.errors.values() for msg in field_errors]
            return jsonify({"success": False, "message": errors})
    else:
        login_form = LoginForm() 
        register_form = RegistrationForm()   
        return render_template('login.html', login_form=login_form,register_form=register_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logs the user out
    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        password = form.password.data
        if check_password_hash(current_user.password, password):
            user = current_user
            # Delete the profile picture if it exists
            if user.profile_picture:
                picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], user.profile_picture)
                if os.path.exists(picture_path):
                    os.remove(picture_path)
            db.session.delete(user)
            db.session.commit()
            logout_user()  # Log out the user after deletion
            return jsonify({"success": True, "redirect": "/"})
        else:
            return jsonify({"success": False, "message": "Password is not correct"})
    else:
        # Form validation failed, return error messages
        errors = [msg for field_errors in form.errors.values() for msg in field_errors]
        return jsonify({"success": False, "message": errors})
      
@app.route('/account')
@login_required
def account():
    profile_picture_form = ProfilePictureForm()
    change_username_form = ChangeUsernameForm() 
    change_password_form = ChangePasswordForm()
    delete_user_form = DeleteUserForm()
    return render_template('account.html', profile_picture_form=profile_picture_form, change_username_form=change_username_form, change_password_form=change_password_form,delete_user_form=delete_user_form)

@app.route('/upload_avatar', methods=['POST'])
@login_required
def upload():
    form = ProfilePictureForm()
    if form.validate_on_submit():
        picture = form.profile_picture.data
        filename = secure_filename(picture.filename)
        
         # Delete the old profile picture if it exists
        if current_user.profile_picture:
            old_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_picture)
            if os.path.exists(old_picture_path):
                os.remove(old_picture_path)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Update user's profile_picture field in the database
        current_user.profile_picture = filename
        db.session.commit()
        return jsonify({"success": True, "redirect": "/account"})
    else:
        # Form validation failed, return error messages
        errors = [msg for field_errors in form.errors.values() for msg in field_errors]
        return jsonify({"success": False, "message": errors})
    

@app.route('/change_username', methods=['POST'])
@login_required
def change_username():
    form = ChangeUsernameForm()
    new_username = form.new_username.data
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            return jsonify({"success": False, "message": "Username already taken. Please choose a different username."})
        new_username = form.new_username.data
        current_user.username = new_username
        db.session.commit()
        return jsonify({"success": True, "message": "Username changed successfully"})
    else:
        # Form validation failed, return error messages
        errors = [msg for field_errors in form.errors.values() for msg in field_errors]
        return jsonify({"success": False, "message": errors})

    

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        user = current_user  # Get the current logged-in user

        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data
        
        if check_password_hash(user.password, current_password):
            # Current password is correct, update the password
            if new_password != confirm_new_password:
                # Check if the new passwords don't match
                flash('Passwords must match', 'password_error')
                return redirect(url_for('account'))  
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password
            db.session.commit()
            return jsonify({"success": True, "message": "Password changed successfully"})
        else:
            return jsonify({"success": False, "message": "Current password is not correct"})
    else:
        # Form validation failed, return error messages
        errors = [msg for field_errors in form.errors.values() for msg in field_errors]
        return jsonify({"success": False, "message": errors})
    

app.run(host='0.0.0.0', port=81)
