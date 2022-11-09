"""Server for movie ratings app."""

from flask import Flask , render_template, request, flash, session, redirect

from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movies/<movie_id>')
def movieinfo(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template('movie_details.html',movie = movie)

@app.route("/movies")
def all_movies():
    movies = crud.get_movies()
    
    return render_template("all_movies.html", movies=movies)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(port= 8000, debug=True)
