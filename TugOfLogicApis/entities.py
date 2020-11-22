


class Game(object):
    gameId = 0
    startTime = ""
    endTime = ""
    numOfPlayer = 0
    isCurrent = False

class User(object):
    userId = 0
    userType = ""
    username = ""
    email = ""
    password = ""
    fullName = ""
    studentClass = ""
    studentNumber = ""
    gamePlayed = 0

class MainClaim(object):
    mainClaimId = 0
    gameId = 0
    statement = ""
    numOfAgree = 0
    numOfDisagree = 0

class ReasonInPlay(object):
    ripId = 0
    mainClaimId = 0
    studentId = 0
    reasonStatement = ""
    description = ""
    logicSide = ""

class Vote(object):
    voteId = 0
    gameId = 0
    userId = 0
    mainClaimId = 0
    ripId = 0
    statementToVote = ""
    voteSide = ""

