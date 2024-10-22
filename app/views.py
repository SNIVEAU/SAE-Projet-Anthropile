from .app import *
from flask import render_template, url_for, redirect
@app.route("/")
def home():
    return render_template("home.html",)