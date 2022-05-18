import os
import sys
import traceback
from flask import Flask, request, render_template, session, redirect

class WorkDir():
    def __init__(self,user_name):
        self.user_name=user_name
    def __enter__(self):
        if not os.path.exists("work"):
            os.mkdir("work")
        if not os.path.exists(f"work\\{self.user_name}"):
            os.mkdir(f"work\\{self.user_name}")
        os.chdir(f"work\\{self.user_name}")
    def __exit__(self, type, value, trace):
        os.chdir("..\\..")


def SetFunctions(app):
    @app.route("/saveCode",methods=("POST",))
    def saveCode():
        user_name = session["userName"]
        code=request.form["code"]
        file_name = request.form["fileName"]
        
        with WorkDir(user_name):
            if os.path.exists(file_name):
                return "file exists"
            with open(file_name,"w") as f:
                f.write(code)
        return "success"


    @app.route("/runCode",methods=("POST",))
    def runCode():
        user_name = session["userName"]
        code=request.form["code"]
        print(code)
        '''
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        if not os.path.exists(f"tmp\\{user_name}"):
            os.mkdir(f"tmp\\{user_name}")
        os.chdir(f"tmp\\{user_name}")

        f1 = open("output","w")
        oldstdout = sys.stdout
        oldstderr = sys.stderr
        sys.stdout = f1
        sys.stderr = f1
        try:
            exec(code)
        except:
            traceback.print_exc()
        finally:
            sys.stdout = oldstdout
            sys.stderr = oldstderr
            f1.close()

            with open("output","r") as f:
                out = f.read()
            print(out)
            os.chdir("..\\..")
            #return out
        '''
        return code
    