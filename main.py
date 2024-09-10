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


from flask import Flask, request, render_template, redirect, url_for
import os
import psycopg2
from psycopg2 import sql


# Initialize Flask app with custom template folder
app = Flask(__name__, template_folder=os.path.abspath('.'))

# Ensure your templates are in a folder named 'templates' in the same directory as this file


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        first_name = request.form['first_name']
        middle_initial = request.form['middle_initial']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        country = request.form['country']

        # Insert data into database
        try:
            conn = psycopg2.connect(os.environ['DATABASE_URL'])
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (first_name, middle_initial, last_name, email, phone_number, street_address, city, state, zip_code, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, middle_initial, last_name, email, phone_number, street_address, city, state, zip_code, country))
            conn.commit()
            cur.close()
            conn.close()
            return "Thank you for signing up!"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while processing your signup. Please try again."

    # If it's a GET request, just render the signup form
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)

