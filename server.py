"""Skills and Job Titles Discovery."""

from passlib.hash import pbkdf2_sha256

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
# from flask_debugtoolbar import DebugToolbarExtension

from model import Users, Skills, UserSkills, connect_to_db, db

import skillsAPI

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")


@app.route("/register")
def reg_form():
    """Renders register form."""

    return render_template("reg_form.html")


@app.route("/register", methods=["POST"])
def reg_process():
    """Takes information from register form and checks if a user with the
       email address exists, and if not, creates a new user in the database."""

    email = request.form.get("email")
    pwd = request.form.get("pwd")

    # https://passlib.readthedocs.io/en/stable/
    pwd_hashed = pbkdf2_sha256.hash(pwd)

    if db.session.query(User).filter(User.email == email).first() is None:
        new_user = User(email=email, password=pwd)
        db.session.add(new_user)
        db.session.commit()

    return redirect("/login-page")


@app.route("/login")  # This is a get request.
def login_page():

    return render_template("login.html")


@app.route("/login", methods=["POST"])  # Post request; can have same route name.
def login_process():
    """Takes information from register form and checks if a user with the
       email address/pwd matches, and if so, logs them in."""

    email = request.form.get("email")
    pwd = request.form.get("pwd")

    # Checks if pwd matches the pwd_hashed in database.
    if pbkdf2_sha256.verify(pwd, pwd_hashed):
        flash("Logged in! as %s" % User.first_name)
        user_id = db.session.query(User.user_id).filter(User.email == email).one()

        session['user_id'] = user_id[0]
        return redirect("/users/%s" % (user_id[0]))
    else:
        flash("Email/password combination do not match.")
        return redirect("/login-page")


@app.route("/logout")
def logout_process():
    """Logs out current user."""

    del session['user_id']
    flash("You are now logged out. Goodbye!")

    return redirect("/")


@app.route("/search_titles")
def titles_query():
    """Takes user search input, retrieves json string and matches job titles to
       database, returns titles and salary information."""

    search_input = request.args.get('search_input')
    titles_list, uuid_list_ignore = skillsAPI.query_titles(search_input)

    return render_template("/related_titles.html", titles=titles_list)

@app.route("/search_skills")
def skills_query():
    """Returns list of skills related to each job title."""

    search_input = request.args.get('search_input')
    skillsAPI.query_skills_from_title(search_input)

    return render_template("/related_skills.html")


# @app.route("/users/<user_id>")
# def show_user_details(user_id):
#     """Shows user details."""

#     user = db.session.query(User).get(user_id)

#     return render_template("user_info.html", user=user)



if __name__ == "__main__":
    # Set app.debug=True since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Makes sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')