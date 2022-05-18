import sqlite3
import json
from flask import Flask, request, render_template, session, redirect

def SetFunctions(app):

    @app.route("/CheckUserName", methods=("POST",))
    def CheckUserName():
        '''检查用户名是否存在'''
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
        '''主页面，登录界面'''
        if session.get("userName") is not None: # 如果已经登录，直接跳转至代码编辑器
            return redirect("/editor")
        return render_template("index.html", login_state="1")


    @app.route("/login", methods=("POST",))
    def login():
        '''登录验证'''
        if session.get("userName") is not None: # 不能重复登录
            return app.send_static_file("repeat_login.html")

        user_name = request.form["user-name"]
        password = request.form["password"]

        # 读取用户密码
        with sqlite3.connect("users.db") as usersDB:
            cur = usersDB.execute(
                "select password from users where name='"+user_name+"'")
            DBpwd = cur.fetchone()

        if DBpwd is None: # 用户不存在
            return render_template("index.html", login_state="user-not-exist")
        if password != DBpwd[0]: # 密码错误
            return render_template("index.html", login_state="password-error")
        
        session["userName"] = user_name

        return redirect("/editor")


    @app.route("/logout")
    def logout():
        '''登出账户'''
        session.clear()
        return redirect("/")


    @app.route("/regis", methods=("POST",))
    def regis():
        '''注册账户'''
        user_name = request.form["user-input"]
        pwd = request.form["pwd"]
        pwd_rp = request.form["pwd_rp"]

        # 读取用户数据库
        with sqlite3.connect("users.db") as usersDB:
            cur = usersDB.execute(
                f"select password from users where name='{user_name}'")
            DBpwd = cur.fetchone()
            if DBpwd is not None: # 用户已存在
                return render_template("register.html", regis_state="user-exist")
            if pwd != pwd_rp: # 两次密码输入不一致
                return render_template("register.html", regis_state="password-error")
            usersDB.execute(
                f"insert into users (name,password) values('{user_name}','{pwd}')")
            usersDB.commit()

        return app.send_static_file("register_success.html")


    @app.route("/register")
    def register():
        '''注册页面'''
        return render_template("register.html", regis_state="")


    @app.route("/editor")
    def editor():
        '''编辑器页面'''
        return app.send_static_file("editor.html")