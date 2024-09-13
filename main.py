#####################
# Welcome to Cursor #
#####################

'''
Step 1: Try generating with Cmd+K or Ctrl+K on a new line. Ask for CLI-based game of TicTacToe.

Step 2: Hit Cmd+L or Ctrl+L and ask the chat what the code does. 
   - Then, try running the code

Step 3: Try highlighting all the code with your mouse, then hit Cmd+k or Ctrl+K. 
   - Instruct it to change the game in some way (e.g. add colors, add a start screen, make it 4x4 instead of 3x3)

Step 4: To try out cursor on your own projects, go to the file menu (top left) and open a folder.
'''


from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
import psycopg2
import base64

# Initialize Flask app with custom template folder
app = Flask(__name__, template_folder=os.path.abspath('.'))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://u422b150ccposr:pdc8a1d1e020d9bb53b0ba7e67746d34f66e92bd19228e0cf5861ad9c12401b2f@cd5gks8n4kb20g.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/df1oegq1p4if0j"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    profile_photo = db.Column(db.LargeBinary)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure your templates are in a folder named 'templates' in the same directory as this file


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        middle_initial = request.form['middle_initial']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone_number']
        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        country = request.form['country']

        # Handle file upload
        profile_photo = request.files['profile_photo']
        if profile_photo and allowed_file(profile_photo.filename):
            profile_photo_data = profile_photo.read()
        else:
            profile_photo_data = None

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert data into database
        try:
            new_user = User(
                first_name=first_name,
                middle_initial=middle_initial,
                last_name=last_name,
                email=email,
                password=hashed_password,
                phone_number=phone_number,
                street_address=street_address,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country,
                profile_photo=profile_photo_data
            )
            db.session.add(new_user)
            db.session.commit()
            return "Thank you for signing up!"
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
            return "An error occurred while processing your signup. Please try again."

    # If it's a GET request, just render the signup form
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Login Failed!', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


# Add this function to make the user available to all templates
@app.context_processor
def inject_user():
    return dict(user=session.get('email'))


if __name__ == '__main__':
    app.run(debug=True)

