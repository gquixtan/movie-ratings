"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import jsonify
from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for)
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Rating, Movie, connect_to_db, db


from model import connect_to_db, db


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
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()
    print movies

    return render_template("movie_list.html", movies=movies)


@app.route("/register", methods=["GET"])
def register_process():
    """what happens after it queries database"""

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_form():
    """Register user"""

    email = request.form.get('email')
    password = request.form.get('password')

    #here we do a db.seession query and bind it to user_email
    user = db.session.query(User).filter(User.email == email).first()
    if user is None:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    else:
        print "Already in database"
        return redirect("/log-in")

    return redirect("/log-in")


@app.route("/log-in", methods=["GET"])
def login_process():
    """User login"""

    return render_template("login.html")


@app.route("/log-in", methods=["POST"])
def log_in():
    """Log in user"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter(User.email == email,
                                         User.password == password).first()

    if user is None:
        return redirect("/register")
    else:
        flash('You were successfully logged in')
        session['user_id'] = user.user_id

        return redirect("/user-detail/"+str(session['user_id']))

@app.route("/rating")
def add_rating():
    """ user adds a rating to a movie """

    # if 'user_id' in session:
    pass



@app.route("/log-out", methods=["GET"])
def log_out():
    """Log out user"""

    if session.get('user_id'):
        del session['user_id']
        flash('You were successfully logged out')
        print session
        return redirect("/")


@app.route("/user-detail/<user_id>")
def render_user(user_id):
    """Render user scores and details"""

    user = User.query.filter_by(user_id=user_id).first()

    return render_template("user_details.html", user_details=user)


@app.route("/movie-detail/<movie_id>")
def render_movie(movie_id):
    """Render movie scores and details"""

    movie = Rating.query.filter_by(movie_id=movie_id).first()

    return render_template("movie_details.html", movie_details=movie)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
