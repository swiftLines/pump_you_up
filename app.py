"""
 * FILENAME: [app.py]
 * AUTHOR: [Jeremy Underwood]
 * COURSE: [SDEV 300]
 * PROFESSOR: [Justin Boswell]
 * CREATEDATE: [07MAY24]

"""

# imports
import logging
import socket
from pathlib import Path
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, url_for, redirect, request, session, flash
from validation.password_complexity import is_password_complex, validate_password, compare, update_password
from validation.user_validation import checknotreg

# create logger variable
logger = logging.getLogger(__name__)
# set level
logger.setLevel(logging.INFO)
# create custom formatter
formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s")
# add to file handler
file_handler = logging.FileHandler("static/faileduser.log")
file_handler.setFormatter(formatter)
# log file
logger.addHandler(file_handler)
ip_address = socket.gethostbyname(socket.gethostname())
logger.error(f'{ip_address} Failed login attempt')

# create an instance of the Flask object
app = Flask(__name__)
# session key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# read the HTML template and return it to the webpage
# URL '/' to be handled by main() route handler (or view function)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function renders the html template
    for the login page and returns
    """
    if request.method == 'POST':
        # Process login form submission
        session['username'] = request.form['username']
        # session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']
        # Path to newdata.txt
        path = Path('static/newdata.txt')
        # Create path object
        print(path.exists())
        # if newdata.txt exist perform check
        if path.exists() and checknotreg(username) == False:
            # check newdata.txt to see if user has reset there password
            with open('static/newdata.txt', 'r') as file:
                content = file.readlines()
                # for every line in the file
                for line in content:
                    text = line.split()
                    if username in text:
                        hash = text[1]
                        # check the entered password against the hashed password
                        if pbkdf2_sha256.verify(password, hash):
                            return redirect(url_for('home'))
        with open(r'static/passfile', 'r') as file:
            content = file.read()
            credentials = f"{username} {password}"
            if credentials in content:
                return redirect(url_for('home'))
            return 'Invalid username or password.'
    return render_template('login.html', date=datetime.now())


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function renders the html template
    for the register page and returns
    """
    if request.method == 'POST':
        # Process registration form submission
        username = request.form['username']
        password = request.form['password']
        if not compare(password):
            message = "This password is most commonly used or compromised"
            return render_template('register.html',date=datetime.now(), error=message)
        # Validate password complexity
        if not is_password_complex(password):
            return 'Password must be at least 12 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.'
        with open('static/passfile', "a") as file:
            file.writelines(f"{username} {password} \n")
        return redirect(url_for('login'))
    return render_template('register.html', date=datetime.now())


# create route for reset page and function to reset
@app.route("/reset", methods=["GET", "POST"])
def reset():
    """
    This function renders an html template
    and returns
    """
    if request.method == "POST":
        # get usernmae and pwd
        username = request.form["username"]
        new_password = request.form["password"]
        # call function to compare pwd with a list
        if not compare(new_password):
            message = "This password is most commonly used or compromised"
            return render_template('reset.html',date=datetime.now(), error=message)
        # validated pwd for pwd requirements
        if not validate_password(new_password):
            message = "Password does not match requirements"
            return render_template("reset.html", date=datetime.now(), error=message)
        # read file
        with open("static/passfile", "r+") as resetfile:
            print('open file')
            resetf = resetfile.readlines()
            # for every line in the file
            for line in resetf:
                text = line.split()
                # if a text[0] is == to the required username
                if text[0] == username:
                    print("In there")
                    # Hash the password
                    hash_pass_new = pbkdf2_sha256.hash(new_password)
                    # replace password
                    repl = line.replace(text[1], hash_pass_new)
                    # call update function
                    update_password(repl)
            # redirect and notify user
            return render_template("reset.html", date=datetime.now(),error="Password changed successfully")
    return render_template("reset.html", date=datetime.now())


@app.route('/home')
def home():
    """
    This function renders the html template
    for the home page and returns
    """
    if 'username' in session:
        return render_template('home.html', date=datetime.now())
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """
    This function releases the session variable and
    renders the html template for the login page and returns
    """
    session.pop('username', None)
    return redirect(url_for('login'))


# register the url for the push page
@app.route('/push')
def push():
    """
    This function renders the html template
    for the push page and returns
    """
    return render_template('push.html', date=datetime.now())


# register the url for the pull page
@app.route('/pull')
def pull():
    """
    This function renders the html template
    for the pull page and returns
    """
    return render_template('pull.html', date=datetime.now())

# if the script is executed run the app
if __name__ == '__main__':
    app.run(debug=True)
