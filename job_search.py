# start with the imports
from sqlalchemy import exc
import pandas as pd
import random
import requests
import json
import pprint
import pdb
import sqlite3
from functools import wraps
from sqlalchemy.types import String
from flask import request, render_template, url_for, flash, redirect, g, jsonify, session
from flask_session import Session
from forms import RegistrationForm

from headers import app, bcrypt
from models import db, User, SavedJob

DATABASE ='./jobify.db'


Session(app)

# '''# interchange use of API Keys to limit searches to not get 100
API_KEYS = ('e21193f2b2ee7a0a7042c7a414822b20b10c84609c42a408732401d8b62ddc06',
            '9e8e77e8075bf5f1bfbbef8848ba3b735d1cf01e0490877307eded9945e41777',
            'c385df59163477b88fa13574e0bb8886c32b687a8eb0b8dded75b959def7262b')

key_index = random.randint(0, 2)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            flash("Error: Need to be logged in to access.", 'error')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def valid_login(username, password):
    user = query_db('select * from user where username = ?', [username], one=True)
    if user is None:
        return False
    hashed_pw = user[2]
    return bcrypt.check_password_hash(hashed_pw, password)

@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('homepage'))

def log_the_user_in(username):
    if session.get('username', None):
        return True
    session['username'] = username
    return redirect(url_for('job_search'))

@app.route("/saved_jobs", methods=('GET', 'POST'))
def save_job():
    #new comment test
    # print(request_data.get('job_title'))
    #get value from checkbox?
    if request.method == 'POST':
        job_id = request.json.get('job_id')
        print(job_id)
        job_title = request.json.get('job_title')
        company_name = request.json.get('company_name')
        job_location = request.json.get('location')
        job_description = request.json.get('description')
        savedjob = SavedJob(username=session['username'],
                            job_id=job_id,
                            job_title=job_title,
                            company_name=company_name,
                            location=job_location,
                            description=job_description)
        print(savedjob)
        db.session.add(savedjob)
        db.session.commit()
        return jsonify(status="success")
        # return render_template(('saved_jobs.html'), job_title=job_title, company_name=company_name, job_location=job_location, job_description=job_description)
        

    # results = {'processed': 'true'}
    # print(jsonify(results))
 
#  results = {'processed': 'true'}
#  return jsonify(results)
#         saved_job = SavedJob(job_title=job_title,company_name=company_name, location=location, description=description)
#         db.session.add(saved_job)
#         db.session.commit()



@app.route("/")
def homepage():
    return render_template('home.html')

@app.route("/job_search", methods=('GET', 'POST'))
@login_required
def job_search():
    if request.method == 'POST':
        try:
            job_fields = request.form['fields']
            job_location = request.form['location']
            #parse info from form into api to get request
            r = requests.get(f'https://serpapi.com/search.json?engine=google_jobs&q={job_fields}&location={job_location}&api_key={API_KEYS[key_index]}')
            data = r.json()['jobs_results']
            return render_template('jobs_list.html', data = data)
        except KeyError:
            return render_template('error.html')
    return render_template('job_search.html')

@app.route("/jobs_list")
@login_required
def jobs_list():
    return render_template('jobs_list.html')


@app.route("/about")
@login_required
def about_page():
    return render_template('about.html')

@app.route("/saved-jobs")
@login_required
def saved_jobs_page():
    engine = db.create_engine('sqlite:///jobify.db', {})
    query = engine.execute(f"SELECT * FROM saved_job WHERE username = '{session['username']}';").fetchall()
    print(query)
    return render_template('saved-jobs.html', jobs = query)

@app.route("/contact")
def contact_page():
    return render_template('contact.html')

@app.route('/register', methods=('GET', 'POST'))
def register_form():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        try:
            hashed_pw = bcrypt.generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
        except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            if 'UNIQUE' in error:
                flash('Unique Error: Username already taken. Please Try again with a Different Username', 'error')
            else:
                flash('Error: Try Again', 'error')
            return redirect(url_for('register_form'))
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('homepage'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    session.clear()
    print(session)
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

    return render_template('login.html', error=error)

@app.route('/delete_job', methods=('GET', 'POST'))
def delete_job():
    if request.method == 'POST':
        print(request.json)
        job_id = request.json.get('job_id')
        job_title = request.json.get('job_title')
        print(job_id)
        engine = db.create_engine('sqlite:///jobify.db', {})
        query = engine.execute(f"DELETE FROM saved_job WHERE job_id = '{job_id}' AND username = '{session['username']}';")
        db.session.commit()
        return render_template('delete_job.html')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    db.create_all()
