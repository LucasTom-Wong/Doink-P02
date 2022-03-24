# Doink!: Lia, LTW, Lisel, Tomas
# P02
# Period 1

from flask import Flask, render_template, request, session, redirect
import sqlite3
from os import urandom
import database

app = Flask(__name__)    #create Flask object

app.secret_key = urandom(24)

tempo_Top = 1;
tempo_Bot = 1;
score = 0;
lives = 3;

def logged_in():
    """
    Returns True if the user is in session.
    """
    return "user" in session

@app.route("/")
def disp_homePage():
    if logged_in():
        return redirect("/home")
    return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect("/home")
    return render_template("login.html")

@app.route("/logout")
def logout():
    """
    Removes user from session.
    """
    if logged_in():
        session.pop("user")
    return redirect("/")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Start
    Retrieves user inputs from signup page.
    Checks it against the database to make sure the information is unique.
    Adds information to the "users" database table.
    """
    if logged_in():
        return redirect("/home")

    # Default page
    # if request.method == "GET":        # else:
    #     #     username = "meow"
    #     #     password = "meow"
    #     return render_template("register.html")
    if len(request.form) == 0:
        return render_template("register.html")

    # Check sign up
    user = request.form["username"]
    pwd = request.form["password"]
    if user.strip() == "" or pwd.strip() == "":
        return render_template("register.html", explain="Username or Password cannot be blank")

    # # Add user information if passwords match
    # if (request.form["password"] != request.form["password"]):
    #     return render_template("register.html", explain="The passwords do not match")

    register_success = database.register_user(user, pwd) #checks if not successful in the database file
    if register_success:
        return redirect("/login")
    return render_template("register.html", explain="Username already exists")
    #goes to register page

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    try:
        # faildadaad
        # if (request.method == 'POST'):
        username = request.form["username"]
        password = request.form["password"] #does it alawys work>>>?????????? who knows
        # else:
        #     username = "meow"
        #     password = "meow"

        if username.strip() == "" or password.strip() == "":
            return render_template("login.html", error = "Username or Password cannot be blank")

        # Verify this user and password exists
        check_info = database.check_login(username, password)
        # print("result:", check_info)
        if check_info is False:
            return render_template("login.html", error = "Username or Password is incorrect")

        # Adds user and user page_id to session if all is well
        session["user"] = username
        return redirect("/")

    except Exception as e:
        username = request.form["username"]
        password = request.form["password"]
        print(username + ": user, " + password + ": pass")
        return render_template("wrong.html", error = e)

@app.route("/home")
def disp_home():
    #check login_method()
    if logged_in(): #later to be replaced with check login
        user = session["user"]
        highscore = database.display_score(user)
        return render_template("home.html", username = user, score = highscore)
    return render_template("wrong.html") #if not logged in, give error

@app.route("/instruct")
def disp_Instructions():
    return render_template("instructions.html") #L

@app.route("/select")
def disp_selectionPage():
    if logged_in():
        global tempo_Top
        global tempo_Bot
        global score
        global lives
        return render_template("selection.html", top=tempo_Top, bot=tempo_Bot, score = score, lives = lives)
    return render_template("wrong.html")

@app.route("/selectTop/<page_id>")
def changeTop(page_id):
    if logged_in():
        global tempo_Top
        tempo_Top = page_id
        return redirect("/select")
    return render_template("wrong.html")

@app.route("/owselectBot/<page_id>")
def changeBot(page_id):
    if logged_in():
        global tempo_Bot
        tempo_Bot = page_id
        return redirect("/select")
    return render_template("wrong.html")


@app.route("/game")
def disp_gamePage():
    if logged_in():
        global tempo_Top
        global tempo_Bot
        global score
        global lives
        render_template("game.html", top = tempo_Top, bot = tempo_Bot, score = score, lives = lives)
    return render_template("wrong.html")

@app.route("/results")
def disp_results():
    if logged_in():
        global score
        old_score = database.display_score(session["user"])
        yay = score > old_score
        if yay:
            database.update_score(session["user"], score)

        render_template("results.html", score = score, newhighscore = yay)
    return render_template("wrong.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
