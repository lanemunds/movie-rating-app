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
def movie_info(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template('movie_details.html',movie = movie)

@app.route("/movies")
def all_movies():
    movies = crud.get_movies()
    
    return render_template("all_movies.html", movies=movies)

@app.route('/users/<user_id>')
def user_info(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html",user = user)

@app.route("/users")
def all_users():
    users = crud.get_users()
    
    return render_template("all_users.html", users=users)

@app.route("/users",methods = ["POST"] )
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if user:
        flash("Account with that email already exists. Please log in or try a different email")
        return redirect('/create_account')
    else:
        user = crud.create_user(email,password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect('/loginpage')    

@app.route("/login", methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session['user_email']= user.email
        flash(f"Welcome Back,{user.email}!")    
    return redirect("/")
   
@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    
    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movies/{movie_id}")

@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    crud.update_rating(rating_id, updated_score)
    db.session.commit()

    return "Success"


@app.route("/logout")
def logout():
    del session['user_email']
    flash("You're logged out")
    return redirect("/")

@app.route("/loginpage")
def login_page():
    return render_template("login.html")

@app.route("/create_account")
def create_account_page():
    return render_template("create_account.html")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(port= 8000, debug=True)

