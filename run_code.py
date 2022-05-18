import os
import sys
import traceback
import json
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

    @app.route("/getFileList",methods=("POST",))
    def getFileList():
        user_name = session["userName"]
        with WorkDir(user_name):
            data=[{"fileName":fileName} for fileName in os.listdir(".\\")]
        jsonData = json.dumps(data, sort_keys=True,
                          indent=4, separators=(',', ': '))
        # print(jsonData)
        return jsonData
    

    @app.route("/getFile",methods=("POST",))
    def getFile():
        user_name = session["userName"]
        file_name = request.form["fileName"]
        with WorkDir(user_name):
            with open(file_name) as f:
                content = f.read()
        return content


    @app.route("/saveCode",methods=("POST",))
    def saveCode():
        user_name = session["userName"]
        code=request.form["code"]
        file_name = request.form["fileName"]
        overWrite = request.form["overWrite"]
        
        with WorkDir(user_name):
            if overWrite=="false" and os.path.exists(file_name):
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
    