"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    # return a

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show a list of users"""

    users = User.query.all()
    return render_template("users_list.html", users=users)

@app.route('/create-user')
def create_user():
    """Render a form for user to create sign in"""

    return render_template("create_user.html")

@app.route('/submit-account', methods=["POST"])
def submit_account():
    """Get email and password, sign-in (if exist), or create new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).all()

    if not user:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    return redirect("/")

@app.route('/login-form')
def log_in():
    """Logs existing user in"""
    return render_template("log_in_form.html")

@app.route('/form-submission')
def submit_form():
    """Submits log-in information"""

    email = request.form.get('email')
    password = request.form.get('password')

    db_password = db.session.query(User.password).filter_by(email=email).all()
    db_user_id = db.session.query(User.user_id).filter_by(email=email).all()

    # if db_password == password:
@app.route('/movies')
def movies_list():

    movies = Movie.query.order_by('title').all()
    return render_template('movies_list.html', movies=movies)

@app.route('/movie/<movie.movie_id>') #is this right?
def show_movie_info():
    """Shows information about a movie"""

    ratings = db.session.query(Movie.ratings).filter_by(movie_id=movie_id).all()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)