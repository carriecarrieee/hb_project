"""Models and database functions for skills database."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class Users(db.Model):
    """Keeps track of web app users."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    pwd_hashed = db.Column(db.String(100))

    skills = db.relationship('Skills',
                             secondary='user_skills',
                             backref='users')

    titles = db.relationship('Titles',
                             secondary='user_titles',
                             backref='users')

    def __repr__(self):
        """Provide helpful representation when printed."""

        user_obj = ("<User ID={user_id} "
                    "name={first} {last} "
                    "email={email}")

        return user_obj.format(user_id=self.user_id,
                               first=self.first_name,
                               last=self.last_name,
                               email=self.email)


class Skills(db.Model):
    """Keeps track of saved skills from user searches."""

    __tablename__ = "skills"

    skill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    skill_name = db.Column(db.String(100))


    def __repr__(self):
        """Provide helpful representation when printed."""

        skill_obj = "<Skills ID={skill_id} skill={skill_name}>"
        return skill_obj.format(skill_id=self.skill_id,
                        skill_name=self.skill_name)


class UserSkills(db.Model):
    """Association table connecting users and their saved skills."""

    __tablename__ = 'user_skills'

    user_skill_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    skill_id = db.Column(db.Integer,
                         db.ForeignKey('skills.skill_id'),
                         nullable=False)


    def __repr__(self):
        """Provide helpful representation of UserSkills when printed."""

        user_skill_obj = ("<UserSkills ID={user_skill_id} "
                         "user ID={user_id} "
                         "skill ID={skill_id}>")

        return user_skill_obj.format(user_skill_id=self.user_skill_id,
                                     user_id=self.user_id,
                                     skill_id=self.skill_id)


class Titles(db.Model):
    """Keeps track of saved titles from user searches."""

    __tablename__ = "titles"

    title_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title_name = db.Column(db.String(64))


    def __repr__(self):
        """Provide helpful representation when printed."""

        title_obj = "<Titles ID={title_id} title={title_name}>"
        return title_obj.format(title_id=self.title_id,
                        title_name=self.title_name)


class UserTitles(db.Model):
    """Association table connecting users and their saved titles."""

    __tablename__ = 'user_titles'

    user_title_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    title_id = db.Column(db.Integer,
                         db.ForeignKey('titles.title_id'),
                         nullable=False)


    def __repr__(self):
        """Provide helpful representation of UserTitles when printed."""

        user_title_obj = ("<UserTitles ID={user_title_id} "
                         "user ID={user_id} "
                         "title ID={title_id}>")

        return user_title_obj.format(user_title_id=self.user_title_id,
                                     user_id=self.user_id,
                                     title_id=self.title_id)


##############################################################################
# Helper functions


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///skills'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
