import os
import sys
import traceback
import json
import subprocess
import io
from flask import Flask, request, render_template, session, redirect
from workdir import WorkDir


def SetFunctions(app):

    @app.route("/getFileList",methods=("POST",))
    def getFileList():
        '''读取用户工作文件夹，获取文件列表，通过json方式返回'''
        user_name = session["userName"]
        with WorkDir(user_name):
            data=[{"fileName":fileName} for fileName in os.listdir(".\\")]
        jsonData = json.dumps(data, sort_keys=True,
                          indent=4, separators=(',', ': '))
        # print(jsonData)
        return jsonData
    

    @app.route("/getFile",methods=("POST",))
    def getFile():
        '''获取特定文件的内容'''
        user_name = session["userName"]
        file_name = request.form["fileName"]
        with WorkDir(user_name):
            with open(file_name) as f:
                content = f.read()
        return content
    

    @app.route("/deleteFile",methods=("POST",))
    def deleteFile():
        '''执行删除文件命令'''
        user_name = session["userName"]
        file_name = request.form["fileName"]
        with WorkDir(user_name):
            os.remove(file_name)
        return ""


    @app.route("/saveCode",methods=("POST",))
    def saveCode():
        '''保存文件：从request读入code和fileName，将code中的代码存进fileName文件里'''
        user_name = session["userName"]
        code=request.form["code"]
        file_name = request.form["fileName"]
        overWrite = request.form["overWrite"]
        
        with WorkDir(user_name):
            if overWrite=="false" and os.path.exists(file_name): # 判断该文件名是否已被使用
                return "file exists"
            with open(file_name,"w") as f:
                f.write(code)
        return "success"


    @app.route("/runCode",methods=("POST",))
    def runCode():
        '''运行代码fileName，并将输出和错误信息一并返回'''
        user_name = session["userName"]
        file_name=request.form["fileName"]
        
        with WorkDir(user_name):
            proc = subprocess.Popen(f"python {file_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
            proc.wait()
            # 设置流，用于获取程序输出
            stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
            stream_stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8')
            
            str_stdout = str(stream_stdout.read())
            str_stderr = str(stream_stderr.read())
            # 防止输出traceback时，服务器内部组织泄露，把所有工作目录替换为'.'
            str_stderr = str_stderr.replace(os.getcwd(),".")
            #print("stdout: " + str_stdout)
            #print("stderr: " + str_stderr)
            
        return str_stdout + str_stderr
    