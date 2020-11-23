from flask_mongoengine import MongoEngine

class db_helper(object):
    #mongodb+srv://<username>:<password>@cluster0.354jx.mongodb.net/tugoflogicdb?retryWrites=true&w=majority
    #Remember to change your mongo atlas user name and password
    DB_URI = 'mongodb+srv://dbjim:bKyDO0W2FASSsfd7@cluster0.354jx.mongodb.net/tugoflogicdb?retryWrites=true&w=majority'

    def get_db_connection(app):
        app.config['MONGODB_HOST'] = db_helper.DB_URI
        db = MongoEngine()
        db.init_app(app)
        return db

