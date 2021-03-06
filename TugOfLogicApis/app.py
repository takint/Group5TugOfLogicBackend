from flask import Flask, render_template, redirect, jsonify, request, make_response
from entities import Games, MainClaims, Votes, Users, ReasonInPlays
from flask_socketio import SocketIO, emit
import helpers.db_helper as dbHelpers
import json

app = Flask(__name__)
socketio = SocketIO(app)
tolDb = dbHelpers.get_db_connection(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/', methods=['GET'])
def init():
    return render_template('index.html')


# Common blocks:
@app.route('/login', methods=['POST'])
def login():
    requestUser = request.get_json()
    user = Users.objects(username=requestUser["username"],
                         password=requestUser["password"]).first()

    if not user:
        return jsonify({'error': 'User and password are invalid!'})
    return jsonify(user)


# End Common blocks

#######################

# Instructor blocks:

###Main Claims###
@app.route('/main-claims', methods=['GET'])
def get_main_claims():
    mc = MainClaims.objects
    return jsonify(mc)

@app.route('/main-claims/<int:mcId>', methods=['GET'])
def get_main_claim(mcId):
    mc = MainClaims.objects(mainClaimId=mcId).first()
    return jsonify(mc)

@app.route('/main-claims-on-game/<int:gameId>', methods=['GET'])
def get_main_claim_on_game(gameId):
    mc = MainClaims.objects(gameId=gameId)
    return jsonify(mc)

@app.route('/add-main-claim', methods=['POST'])
def add_main_claim():
    mainClaim = request.get_json()
    mc = MainClaims(mainClaimId=mainClaim["mainClaimId"],
                    gameId=mainClaim["gameId"],
                    statement=mainClaim["statement"],
                    numOfAgree=mainClaim["numOfAgree"],
                    numOfDisagree=mainClaim["numOfDisagree"])
    mc.save()
    return jsonify(mc)

@app.route('/update-main-claim/<int:mcId>', methods=['PUT'])
def update_main_claim(mcId):
    mc = MainClaims.objects(mainClaimId=mcId).first()
    updatedMainClaim = request.get_json()

    if not mc:
        return jsonify({'error': 'data not found'})
    else:
        mc.update(statement=updatedMainClaim["statement"],
                  numOfAgree=updatedMainClaim["numOfAgree"],
                  numOfDisagree=updatedMainClaim["numOfDisagree"])

    return jsonify(mc)

@app.route('/delete-main-claim/<int:mcId>', methods=['DELETE'])
def delete_main_claim(mcId):
    mc = MainClaims.objects(mainClaimId=mcId).first()

    if not mc:
        return jsonify({'error': 'data not found'})
    else:
        mc.delete()

    return jsonify("MainClaim deleted: OK")


###Games###
@app.route('/games', methods=['GET'])
def get_games():
    games = Games.objects
    isCurrent = request.args.get('isCurrent')

    if isCurrent == 'true':
        isCurrent = True
        return jsonify(Games.objects(isCurrent=isCurrent))
    elif isCurrent == 'false':
        isCurrent = False
        return jsonify(Games.objects(isCurrent=isCurrent))
    else:
        return jsonify(games)

@app.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    game = Games.objects(gameId=id).first()
    return jsonify(game)

@app.route('/add-game', methods=['POST'])
def add_game():
    game = request.get_json()
    newGame = Games(gameId=game["gameId"],
                    startTime=game["startTime"],
                    endTime=game["endTime"],
                    numOfPlayer=game["numOfPlayer"],
                    isCurrent=game["isCurrent"])
    newGame.save()
    return jsonify(newGame)

@app.route('/update-game', methods=['PUT'])
def update_game():
    game = request.get_json()
    updateGame = Games.objects(gameId=game["gameId"]).first()

    if not updateGame:
        return jsonify({'error': 'data not found'})
    else:
        updateGame.update(startTime=game["startTime"],
                          endTime=game["endTime"],
                          numOfPlayer=game["numOfPlayer"],
                          isCurrent=game["isCurrent"])

    return jsonify(updateGame)

@app.route('/delete-game', methods=['DELETE'])
def delete_game():
    game = request.get_json()
    deletedGame = Games.objects(gameId=game["gameId"]).first()
    if not deletedGame:
        return jsonify({'error': 'data not found'})
    else:
        deletedGame.delete()
    return jsonify(deletedGame)


###Users###
@app.route('/users', methods=['GET'])
def get_users():
    users = Users.objects
    return jsonify(users)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = Users.objects(userId=id).first()
    return jsonify(user)

@app.route('/users-in-game/<int:gameId>', methods=['GET'])
def get_users_in_game(gameId):
    user = Users.objects(gamePlayed=gameId)
    return jsonify(user)

@app.route('/add-user', methods=['POST'])
def add_user():
    user = request.get_json()

    newUser = Users(userId=user["userId"],
                    userType=user["userType"],
                    username=user["username"],
                    email=user["email"],
                    password=user["password"],
                    fullName=user["fullName"],
                    studentClass=user["studentClass"],
                    studentNumber=user["studentNumber"],
                    gamePlayed=user["gamePlayed"])

    newUser.save()
    return jsonify(newUser)

@app.route('/update-user', methods=['PUT'])
def update_user():
    user = request.get_json()
    updateUser = Users.objects(userId=user["userId"]).first()

    if not updateUser:
        return jsonify({'error': 'data not found'})
    else:
        updateUser.update(password=user["password"],
                          fullName=user["fullName"],
                          studentClass=user["studentClass"],
                          studentNumber=user["studentNumber"],
                          gamePlayed=user["gamePlayed"])

    return jsonify(updateUser)

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    user = request.get_json()
    deletedUser = Users.objects(userId=user["userId"]).first()

    if not deletedUser:
        return jsonify({'error': 'data not found'})
    else:
        deletedUser.delete()

    return jsonify(deletedUser)


# End instructor blocks

#######################

# Student blocks:

###Reason In Plays###
@app.route('/rips', methods=['GET'])
def get_rips():
    reason = ReasonInPlays.objects
    return jsonify(reason)

@app.route('/rips/<int:id>', methods=['GET'])
def get_rip(id):
    reason = ReasonInPlays.objects(ripId=id).first()
    return jsonify(reason)

@app.route('/rips/<string:username>', methods=['GET'])
def get_rip_by_user(username):
    user = Users.objects(username=username).first()
    reason = ReasonInPlays.objects(studentId=user.userId) if user else ReasonInPlays.objects
    return jsonify(reason)

@app.route('/add-rip', methods=['POST'])
def add_rip():
    reason = request.get_json()
    rip = None

    userRip = Users.objects(username=reason["description"]).first()
    userId = userRip.userId if userRip else 1

    if reason["ripId"] == 0:
        newId = ReasonInPlays.objects.count() + 1
        rip = ReasonInPlays(ripId=newId,
                            mainClaimId=reason["mainClaimId"],
                            studentId=userId,
                            reasonStatement=reason["reasonStatement"],
                            description=reason["description"],
                            logicSide=reason["logicSide"])
        rip.save()
    else:
        rip = ReasonInPlays.objects(ripId=reason["ripId"]).first()
        rip.update(mainClaimId=reason["mainClaimId"],
                    studentId=reason["studentId"],
                    reasonStatement=reason["reasonStatement"],
                    description=reason["description"],
                    logicSide=reason["logicSide"])

    return jsonify(rip)

@app.route('/update-rip', methods=['PUT'])
def update_rip():
    reason = request.get_json()
    rip = ReasonInPlays.objects(ripId=reason["ripId"]).first()

    if not rip:
        return jsonify({'error': 'data not found'})
    else:
        rip.update(reasonStatement=reason["reasonStatement"],
                   description=reason["description"],
                   logicSide=reason["logicSide"])

    return jsonify(rip)

@app.route('/delete-rip/<int:ripId>', methods=['DELETE'])
def delete_rip(ripId):
    rip = ReasonInPlays.objects(ripId=ripId).first()
    if not rip:
        return jsonify({'error': 'data not found'})
    else:
        rip.delete()
    return jsonify("RiP deleted: OK")

###Votes###
@app.route('/votes', methods=['GET'])
def get_votes():
    votes = Votes.objects
    return jsonify(votes)

@app.route('/votes/<int:id>', methods=['GET'])
def get_vote(id):
    vote = Votes.objects(voteId=id).first()
    return jsonify(vote)

@app.route('/add-vote', methods=['POST'])
def add_vote():
    vote = request.get_json()
    newId = Votes.objects.count() + 1
    newVote = Votes(voteId=newId,
                    gameId=vote["gameId"],
                    userId=vote["userId"],
                    mainClaimId=vote["mainClaimId"],
                    ripId=vote["ripId"],
                    statementToVote=vote["statementToVote"],
                    voteSide=vote["voteSide"])

    newVote.save()
    return jsonify(newVote)

@app.route('/update-vote', methods=['PUT'])
def update_vote():
    vote = request.get_json()
    updateVote = Votes.objects(voteId=vote["voteId"]).first()

    if not updateVote:
        return jsonify({'error': 'data not found'})
    else:
        updateVote.update(mainClaimId=vote["mainClaimId"],
                          ripId=vote["ripId"],
                          statementToVote=vote["statementToVote"],
                          voteSide=vote["voteSide"])

    return jsonify(updateVote)

@app.route('/delete-vote', methods=['DELETE'])
def delete_vote():
    vote = request.get_json()
    deleteVote = ReasonInPlays.objects(voteId=vote["voteId"]).first()

    if not deleteVote:
        return jsonify({'error': 'data not found'})
    else:
        deleteVote.delete()

    return jsonify(deleteVote)


### SOCKET IO for Notification and Broadcasting ###

@socketio.on('newRipFromPlayer')
def receive_new_rip_from_student(data):
    emit('newRipFromPlayer', data, broadcast=True)
    
@socketio.on('removeRipFromPlayer')
def remove_rip_from_student(data):
    emit('removeRipFromPlayer', data, broadcast=True)

@socketio.on('newVoteComing')
def receive_new_vote_from_student(data):
    emit('newVoteComing', data, broadcast=True)

@socketio.on('newGame')
def receive_new_game_from_instructor(data):
    # Set all games to passed
    Games.objects.update(isCurrent=False)
    
    # Post only gameId here to current
    Games.objects(gameId=data).update(isCurrent=True)
    Users.objects(userType="Instructor").update(gamePlayed=data)

    # Remove all student users
    Users.objects(userType="Student").delete()

    send_broadcast_message_game_room(data)

@socketio.on('newUser')
def receive_new_user_from_student(data):
    userGame = data.split(':')

    existedUser = Users.objects(username=userGame[0], gamePlayed=userGame[1]).first()
    if not existedUser:
        newId = Users.objects.count() + 1
        newUser = Users(userId=newId,
                    userType="Student",
                    username=userGame[0],
                    email=userGame[0],
                    fullName=userGame[0],
                    gamePlayed=userGame[1])
        newUser.save()
    
    userData = Users.objects(gamePlayed=int(userGame[1])).only('username')
    listUsers = []
    
    for u in userData:
        listUsers.append(u.username)

    send_broadcast_message_user(format(listUsers))

@socketio.on('getRunningGame')
def get_running_game():
    currentSession = request.sid
    gameData = Games.objects(isCurrent=True).only('gameId')
    currentGameIds = []
    
    for g in gameData:
        currentGameIds.append(g.gameId)

    emit('notification_game_room', format(currentGameIds), room = currentSession)


@socketio.on('setCurrentMainClaim')
def set_Current_MainClaim(data):
    print(data)
    emit('notification_current_mainclaim', format(data), broadcast=True)

@socketio.on('startGame')
def startGame(data):
    gameId = data.split(':')[0]
    mcs = data.split(':')[1][:-1]
    selectedMainClaims = mcs.split(',')
    for mc in selectedMainClaims:
        updatedMainClaim = MainClaims.objects(mainClaimId=mc).first()
        updatedMainClaim.update(gameId = gameId)
    emit('notification_startGame', gameId, broadcast=True)

@socketio.on('endGame')
def end_game(data):
    gameData = Games.objects(gameId=data,isCurrent=True)
    for g in gameData:
        g.update(isCurrent=False)
    emit('notification_endGame', data, broadcast=True)

# this would send a message to ALL clients
def send_broadcast_message_game_room(msg):
    emit('notification_game_room', msg, broadcast=True)

# this would send a message to ALL clients
def send_broadcast_message_user(msg):
    emit('notification_user', msg, broadcast=True)

# End student blocks

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=False)

# For debug on windows
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug=False)
