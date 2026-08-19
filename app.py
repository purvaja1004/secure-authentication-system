from flask import Flask, render_template
from routes.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")


@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/forgot-page")
def forgot_page():
    return render_template("forgot_password.html")


@app.route("/reset-page")
def reset_page():
    return render_template("reset_password.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/profile-page")
def profile_page():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)