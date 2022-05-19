# GITHUB

from flask import Flask

app = Flask(__name_)

@app.route("/")
def hello():
    return "Hello World!"