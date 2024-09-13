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
from werkzeug.security import check_password_hash
import os

# Initialize Flask app with custom template folder
app = Flask(__name__, template_folder=os.path.abspath('.'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

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
        password = request.form['password']  # New line to get password
        phone_number = request.form['phone_number']
        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        country = request.form['country']

        # Handle file upload
        profile_photo = request.files['profile_photo']
        if profile_photo:
            # Read the file and encode it
            profile_photo_data = base64.b64encode(profile_photo.read())
        else:
            profile_photo_data = None

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert data into database
        try:
            conn = psycopg2.connect(os.environ['DATABASE_URL'])
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (first_name, middle_initial, last_name, email, password, phone_number, street_address, city, state, zip_code, country, profile_photo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, middle_initial, last_name, email, hashed_password, phone_number, street_address, city, state, zip_code, country, profile_photo_data))
            conn.commit()
            cur.close()
            conn.close()
            return "Thank you for signing up!"
        except Exception as e:
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

