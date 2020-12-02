from flask_mongoengine import MongoEngine
import json

tolDb = MongoEngine()

class MainClaims(tolDb.Document):
    mainClaimId = tolDb.IntField()
    gameId = tolDb.IntField()
    statement = tolDb.StringField()
    numOfAgree = tolDb.IntField()
    numOfDisagree = tolDb.IntField()

    meta = {
        'collection': 'MainClaims'
    }

class Games(tolDb.Document):
    gameId = tolDb.IntField()
    startTime = tolDb.StringField()
    endTime = tolDb.StringField()
    numOfPlayer = tolDb.IntField()
    isCurrent = tolDb.BooleanField()

    userInGame=[]

    meta = {
        'collection': 'Games'
    }

class Users(tolDb.Document):
    userId = tolDb.IntField()
    userType = tolDb.StringField()
    username = tolDb.StringField()
    email = tolDb.StringField()
    password = tolDb.StringField()
    fullName =  tolDb.StringField()
    studentClass = tolDb.StringField()
    studentNumber = tolDb.StringField()
    gamePlayed = tolDb.IntField()

    meta = {
        'collection': 'Users'
    }

class ReasonInPlays(tolDb.Document):
    ripId = tolDb.IntField()
    mainClaimId = tolDb.IntField()
    studentId = tolDb.IntField()
    reasonStatement = tolDb.StringField()
    description = tolDb.StringField()
    logicSide = tolDb.StringField()

    meta = {
        'collection': 'ReasonInPlays'
    }

class Votes(tolDb.Document):
    voteId = tolDb.IntField()
    gameId = tolDb.IntField()
    userId = tolDb.StringField()
    mainClaimId = tolDb.IntField()
    ripId = tolDb.IntField()
    statementToVote = tolDb.StringField()
    voteSide = tolDb.StringField()

    meta = {
        'collection': 'Votes'
    }

