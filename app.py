from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mongodb+srv://vinayakjainlife:suddendeath123@cluster0.efw6gnu.mongodb.net/vvv'  # Change this to a secure key

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
db = client['school_portal']
users_collection = db['users']

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html', user=session['email'])
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email})

        if user and check_password_hash(user['password'], password):
            session['email'] = email
            session['role'] = user['role']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if users_collection.find_one({'email': email}):
            flash('Email already exists', 'error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            users_collection.insert_one({
                'email': email,
                'password': hashed_password,
                'role': role
            })
            flash('Account created successfully!', 'success')
            return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('role', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('signin'))

# Required for Vercel
def handler(event, context):
    return app(event, context)
