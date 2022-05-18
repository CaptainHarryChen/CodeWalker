import os
import sqlite3
import json
from flask import Flask, request, render_template, session, redirect

import user_login
import run_code
import FlowChart

app = Flask(__name__)
user_login.SetFunctions(app) # 设置用户登录相关功能
run_code.SetFunctions(app) # 设置python程序相关功能
FlowChart.SetFunctions(app) # 设置代码转化流程图功能


if __name__ == "__main__":
    app.secret_key = 'ca 0c 86 04 98@ 02b 1b7 8c 88] 1b d7"+ e6px@ c3#\\'
    app.run(host="0.0.0.0", port=80, debug=False)
