from flask import Flask, request, render_template, session, redirect
import os
from workdir import WorkDir


def SetFunctions(app):
    
    @app.route("/flowchart",methods=("GET",))
    def flowchart():
        '''输出特定代码的flowchart的markdown格式'''
        user_name = session["userName"]
        file_name = request.args.get("fileName")
        with WorkDir(user_name):
            with os.popen(f"python -m pyflowchart {file_name}") as f: # 获取该命令的输出
                code = f.read()
        return render_template("flowchart.html",code=code)
