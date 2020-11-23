from flask import Flask, render_template, redirect, jsonify, request, make_response
from helpers.db_helper import db_helper

app = Flask(__name__)
tolDb = db_helper.get_db_connection(app)

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

class MainClaims(tolDb.Document):
    mainClaimId = tolDb.StringField()
    gameId = tolDb.IntField()
    statement = tolDb.StringField()
    numOfAgree = tolDb.IntField()
    numOfDisagree = tolDb.IntField()
    meta = {
        'collection': 'MainClaims'
    }

@app.route('/main-claims')
def get_main_claims():
    mc = MainClaims.objects
    return jsonify(mc)

def get_rips():
    return ""

# End student blocks

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# For debug on windows
#if __name__ == '__main__':
#    import os
#    HOST = os.environ.get('SERVER_HOST', 'localhost')
#    try:
#        PORT = int(os.environ.get('SERVER_PORT', '5000'))
#    except ValueError:
#        PORT = 5000
#    app.run(HOST, PORT)
