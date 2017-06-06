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

import skills_api, elastic

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
        new_user = Users(first_name=fname,
                         last_name=lname,
                         email=email,
                         pwd_hashed=pwd)
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

    # Check if pwd matches the pwd_hashed in database.
    if pbkdf2_sha256.verify(pwd, pwd_hashed):
        
        user = db.session.query(Users).filter(Users.email \
            == email).one()

        session['user_id'] = user.user_id

        # Grab name from User object.

        flash("Logged in! Hello, %s!" % user.first_name)

        return redirect("/welcome")

    elif not user:
        flash("User not found. Please register!")
        return redirect("/reg_form")
    else:
        flash("Email/password combination do not match.")
        return redirect("/")


@app.route("/logout")
def logout():
    """Logs out current user."""

    del session['user_id']
    flash("You are now logged out. Goodbye!")

    return redirect("/")


@app.route("/welcome")
def show_welcome_page():
    """Displays welcome page with search bar and blank U.S. map."""
    
    if session.get('user_id') is None:
        flash("Please login!")
        return redirect("/")
    else:
        user = db.session.query(Users).get(session['user_id'])
        return render_template("/welcome.html", user=user)



@app.route("/dashboard")
def show_skills():
    """Takes user search input and returns titles and related skills."""

    user = db.session.query(Users).get(session['user_id'])
    search_input = request.args.get("search_input")
    # titles, uuid_list_ignore = skillsAPI.get_titles(search_input)

    # skills = skillsAPI.get_skills(search_input)

    return render_template("/dashboard.html",
                            user=user,
                            search_input=search_input)


@app.route("/gmaps_data")
def get_gmaps_data():

    term = request.args.get("search_input")
    print term
    print type(term)

    response = elastic.search_db(term)
    # pprint(response)
    

    results = response["hits"]["hits"]
    # print results
    # for result in results:
    #     latitude = result["_source"]["location"]["lat"]
    #     longitude = result["_source"]["location"]["lon"]
    #     company = str(result["_source"]["TITLE"])

    # print results
    loc_list = []


    # for key, value in results.items():
    #     if latitude not in loc_dict.values():
    #         loc_dict["lat"] = latitude
    #     if longitude not in loc_dict.values():
    #         loc_dict["lng"] = longitude
    #     if company not in loc_dict.values():
    #         loc_dict["emp"] = company
    #     loc_list.append(loc_dict)


    for result in results:
        pprint(result)

        loc_dict = {}
        loc_dict["lat"] = result["_source"]["location"]["lat"]
        loc_dict["lng"] = result["_source"]["location"]["lon"]
        loc_dict["emp"] = str(result["_source"]["EMPLOYER"])

        loc_list.append(loc_dict)
    
    pprint(loc_list)

    # convert_to_set = set()
    # locations = []

    # for item in loc_list:
    #     if tuple([item["lat"], item["lng"], item["emp"]]) not in convert_to_set:
    #         locations.append(item)
    #         convert_to_set.add(tuple([item["lat"], item["lng"], item["emp"]]))

    # pprint(locations)
    return jsonify(loc_list)


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