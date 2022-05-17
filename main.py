import os
import sqlite3
import json
from flask import Flask, request, render_template, session, redirect

import user_login

app = Flask(__name__)
user_login.SetFunctions(app)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=80, debug=True)
