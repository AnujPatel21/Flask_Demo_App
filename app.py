from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'jsdkjskdjskdjskdjksjdskjd'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        users = {}

        if os.path.exists('users.json'):
            with open('users.json') as user_file:
                users = json.load(user_file)

            if request.form['first_name'] in users.keys():
                flash('User already exist')
                return redirect(url_for('home'))

        profile_picture = request.files['profile_picture']
        file_name = request.form['first_name'] + secure_filename(profile_picture.filename)
        profile_picture.save('C:/Users/Anuj Patel/PycharmProjects/flask-demo-app/profile_pictures/' + file_name)

        users[request.form['first_name']] = {
            'last_name': request.form['last_name'],
            'age': request.form['age'],
            'phone_number': request.form['phone_number'],
            'email': request.form['email'],
            'profile_picture': file_name,
            'address': {
                'street_name': request.form['street_name'],
                'city': request.form['city'],
                'state': request.form['state'],
                'zip_code': request.form['zip_code'],
            }
        }
        with open('users.json', 'w') as user_file:
            json.dump(users, user_file)
        return render_template('about.html', first_name=request.form['first_name'])
    else:
        return redirect(url_for('home'))
