import os
from typing import Literal
from cs50 import SQL
from flask import Flask, flash, json, redirect, render_template, request, session, jsonify, Response
from flask.helpers import make_response, url_for
from flask.templating import render_template_string
from flask_session import Session
from tempfile import mkdtemp
from helpers import d, status, login_required
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///50list.db")

app.jinja_env.globals["db"] = db

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        return jsonify({"error": "Please provide an username", "field": "unerror"}), 400

    if not password:
        return jsonify({"error": "Please provide a password", "field": "pwerror"}), 400

    user_row = db.execute("SELECT * FROM users WHERE username = ?", username)

    if not user_row or not check_password_hash(user_row[0]["phash"], password):
        return jsonify({"error": "Invalid username/password", "field": "gerror"}), 400

    session["user_id"] = user_row[0]["id"]

    return jsonify({"url": "/lists"})

@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username:
        return jsonify({"error": "Please provide an username", "field": "unerror"}), 400

    if not password:
        return jsonify({"error": "Please provide a password", "field": "pwerror"}), 400

    if not confirmation:
        return jsonify({"error": "Please provide a confirmation", "field": "cerror"}), 400

    if db.execute("SELECT * FROM users WHERE username = ?", username):
        return jsonify({"error": "Username already taken.", "field": "unerror"}), 400

    if password != confirmation:
        return jsonify({"error": "Password and confirmation do not match", "field": "cerror"}), 400

    phash = generate_password_hash(password)

    db.execute("INSERT INTO users (username, phash) VALUES (?, ?)", username, phash)

    session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]

    return jsonify({"url": "/lists"})

@app.route("/logout", methods=["GET"])
def logout():

    session.clear()

    return redirect("/login")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    return redirect("/lists")

@app.route("/lists", methods=["GET", "POST"])
@app.route("/lists/<name>", methods=["GET", "POST"])
@login_required
def lists(name=None):
    if name:
        if request.method == "POST":
            action = request.form.get("action")
            if action == "delete":
                id = request.form.get("id")
                db.execute("DELETE FROM entries WHERE id = ?", id)
            elif action == "add":
                entry = request.form.get("value")
                if entry != "":
                    list_id = db.execute("SELECT * FROM lists WHERE name = ? ", name)[0]["id"]
                    db.execute("INSERT INTO entries (list, value) VALUES (?, ?)", list_id, entry)
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        list = db.execute("SELECT * FROM lists WHERE owner = ? AND name = ?", user["id"], name)
        try:
            list = list[0]
        except:
            return render_template("404_list.html"), 404
        entries = db.execute("SELECT * FROM entries WHERE list = ?", list["id"])

        return render_template("list.html", entries=entries, name=name, description=list["description"])
    elif request.method == "GET":
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        lists = db.execute("SELECT * FROM lists WHERE owner = ?", user["id"])

        for list in lists:
            list["items"] = len(db.execute("SELECT * FROM entries WHERE list = ?", list["id"]))
            list["created"] = list["created"][:10]
            list["updated"] = list["updated"][:10]
            list["url"] = "/lists/" + list["name"] 

        return render_template("lists.html", lists=lists)

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        list_name = request.form.get("name")
        list_description = request.form.get("description")
        current_lists = db.execute("SELECT * FROM lists WHERE owner = ?", session["user_id"])
        for list in current_lists:
            if list["name"] == list_name:
                return render_template("create.html", error="List name already exists")
        if not list_name:
            return render_template("create.html", error="Please provide a name for your list.")
        if not list_description:
            return render_template("create.html", error="Please provide a description for your list.")
        
        db.execute("INSERT INTO lists (owner, name, description) VALUES (?, ?, ?)", session["user_id"], list_name, list_description)
        return redirect(f"/lists/{list_name}")
