from flask import Flask, render_template, redirect, jsonify, request, make_response
from flask_mongoengine import MongoEngine

app = Flask(__name__)

#"mongodb+srv://<username>:<password>@cluster0.354jx.mongodb.net/tugoflogicdb?retryWrites=true&w=majority"
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://cluster0.354jx.mongodb.net',
    'db': 'tugoflogicdb',
    'username':'<username>',
    'password':'<password>'
}
#Remember to change your mongo atlas user name and password

db = MongoEngine(app)


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def init():
    return render_template('index.html')

# Common blocks:
def login():
    return ""

def logout():
    return ""

def update_votes():
    return ""

# End Common blocks

#######################

# Instructor blocks:

# End instructor blocks

#######################

# Student blocks:

def get_main_claims():
    return ""

def get_rips():
    return ""

# End student blocks

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
