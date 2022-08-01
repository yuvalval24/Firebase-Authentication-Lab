from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import datetime

config = {
  "apiKey": "AIzaSyBXB-K4TQ5nviVvYlCuJMl59leZjnNYsiE",
  "authDomain": "authlaby2s.firebaseapp.com",
  "projectId": "authlaby2s",
  "storageBucket": "authlaby2s.appspot.com",
  "messagingSenderId": "673796120180",
  "appId": "1:673796120180:web:16ecb702a9d71954a87b21",
  "measurementId": "G-VQTV9HG17L",
  "databaseURL" : "https://authlaby2s-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        pas = request.form["password"]
        try:
            login_session["user"] = auth.sign_in_with_email_and_password(email, pas)
            return redirect(url_for("add_tweet"))
        except:
            print("authentication failed signin")
            return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        pas = request.form["password"]
        try:
            user_info = {"email": email, "pas" : pas, "full_name" : request.form["full_name"], "username" : request.form["username"], "bio" : request.form["bio"]}
            login_session["user"] = auth.create_user_with_email_and_password(email, pas)
            print(type(login_session["user"]["localId"]))
            db.child("Users").child(login_session['user']['localId']).set(user_info)
            return redirect(url_for("add_tweet"))
        except:
            print("failed signup")
            return redirect(url_for("signup"))
    else:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        post = {"title": request.form["title"], "text": request.form["text"], "time" :  str(datetime.datetime.now()), "likes":0}
        db.child("Articles").push(post)
    return render_template("add_tweet.html")

@app.route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    if request.method == "POST":
        if request.form["signout"] == "signout":
            login_session["user"] = ""
    return redirect(url_for("signin"))

@app.route("/all_tweets", methods=["post", "get"])
def all_tweet():
    tweet_list = dict(db.child("Articles").get().val())
    key = list(tweet_list.keys())
    if request.method == "POST":
        tweet_list[request.form["like"]]["likes"] += 1
        print(tweet_list[request.form["like"]]["likes"])
        db.child("Articles").update(tweet_list)
        pass
    return render_template("tweets.html", tweet_list = tweet_list, keys=key)

if __name__ == '__main__':
    app.run(debug=True)