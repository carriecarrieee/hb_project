"""Skills and Job Titles Discovery."""

from passlib.hash import pbkdf2_sha256

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Users, Skills, Titles, UserSkills, UserTitles, connect_to_db, db

import skillsAPI

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
        new_user = Users(email=email, pwd_hashed=pwd_hashed)
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
        return redirect("/dashboard/%s" % (user_id[0]))
    else:
        flash("Email/password combination do not match.")
        return redirect("/")


@app.route("/logout")
def logout():
    """Logs out current user."""

    del session['user_id']
    flash("You are now logged out. Goodbye!")

    return redirect("/")


@app.route("/dashboard/<user_id>")
def show_skills(user_id):
    """Takes user search input and returns titles and related skills."""

    user = db.session.query(User).get(user_id)
    search_input = request.args.get("search_input")
    titles_list, uuid_list_ignore = skillsAPI.get_titles(search_input)

    skills = get_skills("search_input")

    return render_template("/dashboard/%s.html" % (user_id[0]),
                            user=user,
                            titles=titles_list,
                            skills=skills_list)


@app.route("/users/<user_id>")
def show_user_details(user_id):
    """Shows user details."""

    user = db.session.query(User).get(user_id)

    return render_template("user_info.html", user=user)



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