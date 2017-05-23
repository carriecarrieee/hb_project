"""Utility file to seed salaries database."""

from sqlalchemy import func
from model import Users, Skills, UserSkills, Titles, UserTitles

from model import connect_to_db, db
from server import app


def load_salaries():
    """Load data from h1b file into salaries database."""

    print "Salaries"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Salaries.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/hlb_salaries"):
        row = row.rstrip().split('","')
  
        employer_name, soc_name, job_title, wage, lon, lat = row[1], row[2], row[3], row[4], row[7], row[8]


        salary_obj = Salaries(employer=employer_name,
                              soc=soc_name,
                              title=job_title,
                              salary=wage,
                              lon=lon,
                              lat=lat)

        # We need to add to the session or it won't ever be stored
        db.session.add(salary_obj)

    # Once we're done, we should commit our work
    db.session.commit()


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the max user_id in the database so there won't be overlaps/overwrites.
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them.
    db.create_all()

    # Import different types of data
    # load_users()
    # load_skills()
    # load_user_skills()
    # set_val_user_id()
