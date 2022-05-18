import sqlite3
import json
from flask import Flask, request, render_template, session, redirect

def SetFunctions(app):

    @app.route("/CheckUserName", methods=("POST",))
    def CheckUserName():
        user_name = request.form["user_name"]
        with sqlite3.connect("users.db") as usersDB:
            cur = usersDB.execute(
                "select password from users where name='"+user_name+"'")
            DBpwd = cur.fetchone()

        if DBpwd is None:
            return "1"
        return "0"

    @app.route("/")
    def index():
        if session.get("userName") is not None:
            return redirect("/editor")
        return render_template("index.html", login_state="1")


    @app.route("/login", methods=("POST",))
    def login():
        if session.get("userName") is not None:
            return app.send_static_file("repeat_login.html")

        user_name = request.form["user-name"]
        password = request.form["password"]

        with sqlite3.connect("users.db") as usersDB:
            cur = usersDB.execute(
                "select password from users where name='"+user_name+"'")
            DBpwd = cur.fetchone()

        if DBpwd is None:
            return render_template("index.html", login_state="user-not-exist")
        if password != DBpwd[0]:
            return render_template("index.html", login_state="password-error")
        
        session["userName"] = user_name

        return redirect("/editor")


    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")


    @app.route("/regis", methods=("POST",))
    def regis():
        user_name = request.form["user-input"]
        pwd = request.form["pwd"]
        pwd_rp = request.form["pwd_rp"]

        with sqlite3.connect("users.db") as usersDB:
            cur = usersDB.execute(
                f"select password from users where name='{user_name}'")
            DBpwd = cur.fetchone()
            if DBpwd is not None:
                return render_template("register.html", regis_state="user-exist")
            if pwd != pwd_rp:
                return render_template("register.html", regis_state="password-error")
            usersDB.execute(
                f"insert into users (name,password) values('{user_name}','{pwd}')")
            usersDB.commit()

        return app.send_static_file("register_success.html")


    @app.route("/register")
    def register():
        return render_template("register.html", regis_state="")


    @app.route("/editor")
    def chat():
        return app.send_static_file("editor.html")