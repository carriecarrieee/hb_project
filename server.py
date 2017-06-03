"""Skills and Job Titles Discovery."""

from passlib.hash import pbkdf2_sha256

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Users, Skills, Titles, UserSkills, UserTitles, connect_to_db, db

from elasticsearch import Elasticsearch

from pprint import pprint

import requests, json

import skillsAPI, elastic

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def home():
    """Homepage."""

    return render_template("home.html")


@app.route("/reg_form")
def reg_form():
    """Renders register form."""

    return render_template("reg_form.html")


@app.route("/register", methods=["POST"])
def reg_process():
    """Takes information from register form and checks if a user with the
       email address exists, and if not, creates a new user in the database."""

    fname = request.form.get("firstname")
    lname = request.form.get("lastname")
    email = request.form.get("email")
    pwd = request.form.get("pwd")

    # https://passlib.readthedocs.io/en/stable/
    pwd_hashed = pbkdf2_sha256.hash(pwd)

    if db.session.query(Users).filter(Users.email == email).first() is None:
        new_user = Users(fname=fname,
                         lname=lname,
                         email=email,
                         pwd_hashed=pwd_hashed)
        db.session.add(new_user)
        db.session.commit()

    return redirect("/")


@app.route("/login", methods=["POST"])  # Post request
def login():
    """Takes information from register form and checks if a user with the
       email address/pwd matches, and if so, logs them in."""

    email = request.form.get("email")
    pwd = request.form.get("pwd")

    pwd_hashed = db.session.query(Users).filter(Users.email \
        == email).first().pwd_hashed

    # Checks if pwd matches the pwd_hashed in database.
    if pbkdf2_sha256.verify(pwd, pwd_hashed):
        flash("Logged in! as %s" % Users.first_name)
        user_id = db.session.query(Users.user_id).filter(Users.email \
            == email).one()

        session['user_id'] = user_id[0]
        return redirect("/welcome/%s" % session['user_id'])
    else:
        flash("Email/password combination do not match.")
        return redirect("/")


@app.route("/logout")
def logout():
    """Logs out current user."""

    del session['user_id']
    flash("You are now logged out. Goodbye!")

    return redirect("/")


@app.route("/welcome/<user_id>")
def show_welcome_page(user_id):
    """Displays welcome page with search bar and blank U.S. map."""
    
    user = db.session.query(Users).get(user_id)

    return render_template("/welcome.html", user=user)


@app.route("/dashboard")
def show_skills():
    """Takes user search input and returns titles and related skills."""

    user = db.session.query(Users).get(session["user_id"])
    search_input = request.args.get("search_input")
    # titles, uuid_list_ignore = skillsAPI.get_titles(search_input)

    # skills = skillsAPI.get_skills(search_input)

    titles = ["testing titles"]
    skills = ["testing skills"]

    return render_template("/dashboard.html",
                            user=user,
                            titles=titles,
                            skills=skills)

@app.route("/gmaps_data")
def get_gmaps_data():

    skill = request.args.get("skill")
    print skill
    # loc_list = []
    # loc_dict = {}
    # # lat_lon_set = 

    # response = elastic.search_db(skill)
    # results = response["hits"]["hits"]
    # for result in results:
    #     # if 
    #     loc_dict["lat"] = result["_source"]["location"]["lat"]
    #     loc_dict["lng"] = result["_source"]["location"]["lon"]
    #     loc_dict["title"] = str(result["_source"]["TITLE"])
    #     loc_list.append(loc_dict)

    mock_data = [
        {"lat": -31.563910, "lng": 147.154312},
        {"lat": -33.718234, "lng": 150.363181},
        {"lat": -33.727111, "lng": 150.371124},
        {"lat": -33.848588, "lng": 151.209834},
        {"lat": -33.851702, "lng": 151.216968},
        {"lat": -34.671264, "lng": 150.863657},
        {"lat": -35.304724, "lng": 148.662905},
        {"lat": -36.817685, "lng": 175.699196},
        {"lat": -36.828611, "lng": 175.790222},
        {"lat": -37.750000, "lng": 145.116667},
        {"lat": -37.759859, "lng": 145.128708},
        {"lat": -37.765015, "lng": 145.133858},
        {"lat": -37.770104, "lng": 145.143299},
        {"lat": -37.773700, "lng": 145.145187},
        {"lat": -37.774785, "lng": 145.137978},
        {"lat": -37.819616, "lng": 144.968119},
        {"lat": -38.330766, "lng": 144.695692},
        {"lat": -39.927193, "lng": 175.053218},
        {"lat": -41.330162, "lng": 174.865694},
        {"lat": -42.734358, "lng": 147.439506},
        {"lat": -42.734358, "lng": 147.501315},
        {"lat": -42.735258, "lng": 147.438000},
        {"lat": -43.999792, "lng": 170.463352}
    ]

    # pprint(loc_list)
    return jsonify(mock_data)




if __name__ == "__main__":
    # Set app.debug=True since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Makes sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')