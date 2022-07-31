from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBXB-K4TQ5nviVvYlCuJMl59leZjnNYsiE",
  "authDomain": "authlaby2s.firebaseapp.com",
  "projectId": "authlaby2s",
  "storageBucket": "authlaby2s.appspot.com",
  "messagingSenderId": "673796120180",
  "appId": "1:673796120180:web:16ecb702a9d71954a87b21",
  "measurementId": "G-VQTV9HG17L",
  "databaseURL" : ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        pas = request.form["password"]
        try:
            print("authentication succeeded signin")
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
            login_session["user"] = auth.create_user_with_email_and_password(email, pas)
            return redirect(url_for("add_tweet"))
        except:
            print("authentication failed")
    else:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        if request.form["signout"] == "signout":
            login_session["user"] = ""
            return redirect(url_for("signup"))
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)