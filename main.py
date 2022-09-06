import json
import psycopg2
import config

from functools import cache
from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth
from google.cloud import storage

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = config.SECRET_KEY

oauth = OAuth(app, cache=cache)

storage_client = storage.Client.from_service_account_json(config.GOOGLE_BUCKET_JSON)
bucket = storage_client.get_bucket(config.GOOGLE_BUCKET_NAME)
bucket_path = config.GOOGLE_BUCKET_PATH

google = oauth.register(
    name='google',
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url=config.GOOGLE_DISCOVERY_URL,
)

github = oauth.register(
    name='github',
    client_id=config.GITHUB_CLIENT_ID,
    client_secret=config.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


def get_db_connection():
    conn = psycopg2.connect(host='35.185.116.190',
                            database='postgres',
                            user=config.DB_USER,
                            password=config.DB_PASSWORD)
    return conn


# Login page route
@app.route("/")
def index():
    return render_template('index.html')


# Google login route
@app.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM person;')
    users = cur.fetchall()
    for user in users:
        if resp['email'] == user[4]:
            flash('You are successfully logged in')
            return redirect('/home')
    flash('User account not found')
    return redirect('/')


# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# Github authorize route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM person;')
    users = cur.fetchall()
    for user in users:
        if resp['email'] == user[4]:
            flash('You are successfully logged in')
            return redirect('/home')
    flash('User account not found')
    return redirect('/')


# Logout route
@app.route("/logout")  # the logout page and function
def logout():
    session.clear()
    return redirect("/")


# Homepage route
@app.route('/home')
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM person;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('home.html', users=users, bucket_path=bucket_path)


# create user route
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        file_name = ''

        if request.files:
            profile_picture = request.files['profile_picture']

            if profile_picture.filename != "":
                file_name = "%s/%s_%s" % (
                    'profile_pictures', request.form['first_name'].strip(), secure_filename(profile_picture.filename))
                blob = bucket.blob(file_name)
                blob.upload_from_file(profile_picture)

        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name']
        age = request.form['age']
        email = request.form['email']
        profile_picture = file_name,
        address = {
            'street_name': request.form['street_name'],
            'city': request.form['city'],
            'state': request.form['state'],
            'zip_code': request.form['zip_code']
        }
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO person (first_name, last_name, age, email, address, profile_picture)'
                    'VALUES (%s, %s, %s, %s, %s, %s)',
                    (first_name, last_name, age, email, json.dumps(address), profile_picture))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('home'))
    else:
        return render_template('create_user.html')


# User detail route
@app.route('/get_user/<int:user_id>')
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    select_query = 'SELECT * FROM person where id=%s;'
    cur.execute(select_query, (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user is not None:
        return render_template('user_detail.html', user=user, bucket_path=bucket_path)
    return abort(404)


# 404 route
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    app.run(port=5000)
