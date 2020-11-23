from flask import Flask, render_template, redirect, jsonify, request, make_response
from flask_mongoengine import MongoEngine

app = Flask(__name__)

#mongodb+srv://<username>:<password>@cluster0.354jx.mongodb.net/tugoflogicdb?retryWrites=true&w=majority
#Remember to change your mongo atlas user name and password
app.config['MONGODB_HOST'] = 'mongodb+srv://dbjim:bKyDO0W2FASSsfd7@cluster0.354jx.mongodb.net/tugoflogicdb?retryWrites=true&w=majority'

db = MongoEngine()
db.init_app(app)

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

class MainClaims(db.Document):
    mainClaimId = db.StringField()
    gameId = db.IntField()
    statement = db.StringField()
    numOfAgree = db.IntField()
    numOfDisagree = db.IntField()
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
