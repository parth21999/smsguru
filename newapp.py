from flask import Flask
application = app = Flask(__name__)

@app.route('/', method="GET")
def get_homepage():
    return "Hello, World"