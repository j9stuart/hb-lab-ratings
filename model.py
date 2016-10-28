"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id= {} email={}>".format(self.user_id, self.email)

    def similarity(self, other):
        """Provides similarity between users"""
        user_ratings = {}
        pairs = []

        u_ratings = self.ratings
        o_ratings = other.ratings

        for rating in u_ratings:
            user_ratings[rating.movie_id]=rating

        for o_rating in o_ratings:
            u_rating = user_ratings.get(o_rating.movie_id)
            if u_rating is not None:
                pair = (u_rating.score, o_rating.score)
                pairs.append(pair)

        if pairs:
            return correlation.pearson(pairs)

        else:
            return 0.0

    def predict_rating(self, movie):
        """Predict a user's rating of a movie."""

        other_ratings = movie.ratings
        other_users = [ r.user for r in other_ratings ]

        similarities = [
            (self.similarity(other_user), other_user.ratings)
            for other_user in other_users
        ]

        similarities.sort(reverse=True)

        coefficients, ratings = zip(*similarities)

        sum_coeff_ratings = 0

        for i in range(len(coefficients)):
            product = coefficients[i] * ratings[i]
            sum_coeff_ratings += product


        mean = sum_coeff_ratings / sum(coefficients)

        return mean






# Put your Movie and Rating model classes here.
class Movie(db.Model):
    """Movie information"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(160), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Movie movie_id= {} title={} released_at={}>".format(self.movie_id, self.title, self.released_at)



class Rating(db.Model):
    """Rating Information"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('ratings', order_by=rating_id))
    movie = db.relationship('Movie', backref=db.backref('ratings', order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>"
        return s % (self.rating_id, self.movie_id, self.user_id, self.score)




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
