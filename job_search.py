# start with the imports
from sqlalchemy import exc
import pandas as pd
import random
import requests
import json
from pprint import pprint
import pdb
import sqlite3
from functools import wraps
from sqlalchemy.types import String
from flask import request, render_template, url_for, flash, redirect, g, jsonify, session
from flask_session import Session
from forms import RegistrationForm, ResumeForm
from flask_behind_proxy import FlaskBehindProxy

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
    try:
        user = query_db('select * from user where username = ?', [username], one=True)
        if user is None:
            return False
        hashed_pw = user[2]
        return bcrypt.check_password_hash(hashed_pw, password)
    except ValueError as e:
        flash("Invalid login")

@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('homepage'))

def log_the_user_in(username):
    if session.get('username', None):
        return True
    session['username'] = username
    return redirect(url_for('job_search'))


def exp_counter(form_data):
    i = 1
    while True:
        try:
            temp = form_data[f"company {i + 1}"]
        except KeyError:
            break
        else:
            i += 1
    return i

@app.route("/saved_jobs", methods=('GET', 'POST'))
def save_job():
    #new comment test
    # print(request_data.get('job_title'))
    #get value from checkbox?
    if request.method == 'POST':
        job_id = request.json.get('job_id')
        source_link = link_finder(job_id)
        job_title = request.json.get('job_title')
        company_name = request.json.get('company_name')
        job_location = request.json.get('location')
        job_description = request.json.get('description')
        savedjob = SavedJob(username=session['username'],
                            job_id=job_id,
                            job_title=job_title,
                            company_name=company_name,
                            location=job_location,
                            description=job_description,
                            job_links = source_link)
        print(savedjob)
        db.session.add(savedjob)
        db.session.commit()
        return jsonify(status="success")
        # return render_template(('saved_jobs.html'), job_title=job_title, company_name=company_name, job_location=job_location, job_description=job_description)

@app.route("/resume-builder", methods=('GET', 'POST'))
def resume_builder():
    form = ResumeForm()
    if request.method == 'POST':
        # for item in request.form.items():
        #     print(item)
        data = {k:v for k,v in request.form.items()}
        num_experience = exp_counter(data)
        return render_template('resume_display.html', data = data, num_exp = num_experience) # request.json().
    return render_template('resume-builder.html', form = form)

# def fill_out_form():
#     for each div in the request:
#         form.skill[i] = StringField(and so on)

# @app.route("/resume_display", methods=('GET', 'POST'))
# def resume_display():
#     # form = ResumeForm()
#     print(form.name.data)
#     flash(form.errors)
#     if form.validate_on_submit() and request.method == 'POST':
#         # print(form.name.data)
#         # print(form.email.data)
#         # print(request.form.get('phone_number'))
#         # print(request.form.get('skill_title1'))
#         # print(request.form.get('skill_description1'))
#         # print(request.form.get('skill_title2'))
#         # print(request.form.get('skill_description2'))
#         # print(request.form.get('skill_title3'))
#         # print(request.form.get('skill_description3'))
#         # print(request.form.get('relevant_skill1'))
#         # print(request.form.get('company1'))
#         # print(request.form.get('major'))
#         # print(request.form.get('company1'))

#         # # try:
#         # name = form.name.data
#         # title = form.title.data
#         # email = form.email.data
#         # phone_number = form.phone_number.data
#         # education = form.education.data
#         # education_address = form.education_address.data
#         # major = form.major.data
#         # gpa = form.gpa.data
#         # skill_title1 = form.skill_title1.data
#         # skill_description1 = form.skill_description1.data
#         # skill_title2 = form.skill_title2.data
#         # skill_description2 = form.skill_description2.data
#         # skill_title3 = form.skill_title3.data
#         # skill_description3 = form.skill_description3.data
#         # #relevant skills
#         # relevant_skill1 =  form.relevant_skill1.data
#         # relevant_skill2 =  form.relevant_skill2.data
#         # relevant_skill3 =  form.relevant_skill3.data
#         # relevant_skill4 =  form.relevant_skill4.data
#         # relevant_skill5 =  form.relevant_skill5.data
#         # relevant_skill6 =  form.relevant_skill6.data
#         # relevant_skill7 =  form.relevant_skill7.data
#         # relevant_skill8 =  form.relevant_skill8.data
#         # relevant_skill9 =  form.relevant_skill9.data
#         # relevant_skill10 =  form.relevant_skill10.data
#         # #professional exeperince section
#         # company1 = form.company1.data
#         # position1 = form.position1.data
#         # position_description1 = form.position_description1.data
#         # start_date1 = form.start_date1.data
#         # end_date1 = form.end_date1.data

#         # company2 = form.company2.data
#         # position2 = form.position2.data
#         # position_description2 = form.position_description2.data
#         # start_date2 = form.start_date2.data
#         # end_date2 = form.end_date2.data

#         # company3 = form.company3.data
#         # position3 = form.position3.data
#         # position_description3 = form.position_description3.data
#         # start_date3 = form.start_date3.data
#         # end_date3 = form.end_date3.data

#         # company4 = form.company4.data
#         # position4 = form.position4.data
#         # position_description4 = form.position_description4.data
#         # start_date4 = form.start_date4.data
#         # end_date4 = form.end_date4.data

#         # company5 = form.company5.data
#         # position5 = form.position5.data
#         # position_description5 = form.position_description5.data
#         # start_date5 = form.start_date5.data
#         # end_date5 = form.end_date5.data

#         # #Affiliations/Interests Tab
#         # affiliations = form.affiliations.data
#         # certifications = form.certifications.data
#         # awards = form.awards.data
#         # interests = form.interests.data
#         # publications = form.publications.data
#         # volunteer = form.volunteer.data 
#         # except:
#         #     flash('Error: Key information missing')
#         return render_template('resume_display.html', form = form)

#         # return render_template('resume_display.html', name = name, title = title, email = email,
#             # phone_number = phone_number, education = education,
#             # major = major, gpa = gpa, education_address = education_address,
#             # skill_title1 = skill_title1, skill_description1 = skill_description1,
#             # skill_title2 = skill_title2, skill_description2 = skill_description2,
#             # skill_title3 = skill_title3, skill_description3 = skill_description3,
#             # relevant_skill1 =  relevant_skill1, relevant_skill2 =  relevant_skill2,
#             # relevant_skill3 =  relevant_skill3, relevant_skill4 =  relevant_skill4,
#             # relevant_skill5 =  relevant_skill5, relevant_skill6 =  relevant_skill6,
#             # relevant_skill7 =  relevant_skill7, relevant_skill8 =  relevant_skill8,
#             # relevant_skill9 =  relevant_skill9, relevant_skill10 =  relevant_skill10,
#             # company1 = company1, position1 = position1, 
#             # position_description1 = position_description1,
#             # start_date1 = start_date1, end_date1 = end_date1, company2 = company2, 
#             # position2 = position2,
#             # position_description2 = position_description2, start_date2 = start_date2, 
#             # end_date2 = end_date2, company3 = company3, position3 = position3,
#             # position_description3 = position_description3,
#             # start_date3 = start_date3, end_date3 = end_date3,company4 = company4, 
#             # position4 = position4, position_description4 = position_description4, 
#             # start_date4 = start_date4, end_date4 = end_date4,
#             # company5 = company5, position5 = position5,
#             # position_description5 = position_description5, start_date5 = start_date5,
#             # end_date5 = end_date5, affiliations = affiliations,
#             # certifications = certifications, awards = awards, interests = interests,
#             # publications = publications, volunteer = volunteer )
#     else:
#         flash('Error: Key information missing')
#         return render_template('resume-builder.html', form=form)
    

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
        job_id = request.json.get('job_id')
        engine = db.create_engine('sqlite:///jobify.db', {})
        query = engine.execute(f"DELETE FROM saved_job WHERE job_id = '{job_id}' AND username = '{session['username']}';")
        db.session.commit()
        return render_template('delete_job.html')


def link_finder(job_id):
    print(job_id)
    request = requests.get(f'https://serpapi.com/search.json?engine=google_jobs_listing&q={job_id}&api_key={API_KEYS[key_index]}')
    print(request.json())
    try:
        apply_link = request.json()["apply_options"]
        title = apply_link[0]['title']
        link = apply_link[0]['link']
        return f"{title} : {link}"
    except KeyError:
        try:
            salary_data = request.json()["salaries"]
            link = salary_data[0]['link']
            source = salary_data[0]['source']
            return f"{source} : {link}"
        except KeyError:
            return None
    



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    db.create_all()


            #  list_data.append(link_data)
        #  for i in range(len(list_data)):
        #      print(f'job {i + 1}:')
        #      for j in range(len(list_data[i])):
        #          for key, value in list_data[i][j].items():
        #              if key == 'link' and j <= 3:
                         