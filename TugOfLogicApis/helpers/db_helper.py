from flask_mongoengine import MongoEngine

#mongodb+srv://<username>:<password>@cluster0.354jx.mongodb.net/tugoflogicdb?retryWrites=true&w=majority
#Remember to change your mongo atlas user name and password
DB_URI = 'mongodb+srv://dbjim:bKyDO0W2FASSsfd7@cluster0.354jx.mongodb.net/tugoflogicdb?retryWrites=true&w=majority'

def get_db_connection(app):
    app.config['MONGODB_HOST'] = DB_URI
    db = MongoEngine()
    db.init_app(app)
    return db

