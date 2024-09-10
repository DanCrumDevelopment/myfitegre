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


from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash, check_password_hash
import base64

# Initialize Flask app with custom template folder
app = Flask(__name__, template_folder=os.path.abspath('.'))
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.secret_key = os.urandom(24)  # Set a secret key for session management

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

        try:
            conn = psycopg2.connect(os.environ['DATABASE_URL'])
            cur = conn.cursor()
            cur.execute("SELECT id, email, password FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['email'] = user[1]
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'error')
        except Exception as e:
            print(f"An error occurred: {e}")
            flash('An error occurred while processing your login. Please try again.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    flash('Logged out successfully!', 'success')
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

