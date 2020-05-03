from app import app, db
from app.tables import Player, Game, Character
from flask import Flask, render_template, redirect, request, url_for
import uuid 
from datetime import datetime
import time

  
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        id = uuid.uuid4()
        response = redirect(url_for("home"))
        response.set_cookie('SessionCookie', id.hex)
        return response
    else:
        print("You're in!")

    return render_template('home.html')

@app.route('/createuser', methods=['POST'])
def create_user():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        return redirect(url_for("home"))
    elif get_game_id(user_id):
        return render_template('home.html', error = "You are already in a game. Please rejoin it through Join Game.")
    else:
        game_id = request.form["game"]
        player_name = request.form["name"]
        create = request.form["create"]
        if create == "create":
            game = Game(id=game_id)
            Player(name=player_name, id = user_id, game=game)
            db.session.add(game)
            db.session.commit()
            return redirect(url_for("wait", state="char"))
        else:
            game = Game.query.filter_by(id=game_id).first()
            Player(name=player_name, id = user_id, game=game)
            db.session.add(game)
            db.session.commit()
            return redirect(url_for("wait", state="char"))

@app.route('/creategame')
def create_game():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        return redirect(url_for("home"))
    else:
        id = uuid.uuid4()
        return render_template('creategame.html', data=id.hex)

@app.route('/joingame')
def join_game():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        return redirect(url_for("home"))
    else:
        return render_template('joingame.html', game_id = get_game_id(user_id))

@app.route('/wait')
def wait():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        return redirect(url_for("home"))
    if 'state' in request.args:
        if request.args['state'] == "game":
            return render_template('wait.html', state = "game")
        else:
            return render_template('wait.html', state = "char")
    return render_template('wait.html')

@app.route('/enternames')
def enter_names():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        return redirect(url_for("home"))
    else:
        return render_template('enternames.html')

@app.route('/addnames', methods=['POST'])
def add_names():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        return redirect(url_for("home"))

    game_id = get_game_id(user_id)
    if game_id:
        name1 = request.form["name1"]
        name2 = request.form["name2"]
        name3 = request.form["name3"]
        player = Player.query.filter_by(id=user_id).first()
        player.enter = "1"
        game = Game.query.filter_by(id=game_id).first()
        total = 0
        for player in game.players:
            total += int(player.enter)
        if total == len(game.players):
            game.state = "2"
            game.starttime = str(time.time() + 60)
        else:
            game.state = "1"
        Character(name=name1, id = user_id+name1, game=game)
        Character(name=name2, id = user_id+name2, game=game)
        Character(name=name3, id = user_id+name3, game=game)
        db.session.add(game)
        db.session.commit()
        return redirect(url_for("wait", state="game"))
    else:
        return render_template('home.html', error = "You are already in a game. Please rejoin it through Join Game.")
        

@app.route('/gameinfo')
def game_info():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    data = {}
    if user_id == None:
        return data
    else:
        player = Player.query.filter_by(id=user_id).first()

        if player is not None:
            game_id = player.game_id

            game = Game.query.filter_by(id=game_id).first()

            data["id"] = game.id
            data["state"] = game.state
            data["individual"] = {"name": player.name, "id": player.id, "ready": player.enter}

            data["players"] = {}
            for player in game.players:
                data["players"][player.name] = {"id": player.id, "ready": player.enter}

            data["characters"] = {}
            for character in game.characters:
                data["characters"][character.name] = character.id

        return data

@app.route('/game')
def game():
    user_id = request.cookies.get('SessionCookie')
    print(user_id)
    if user_id == None:
        return render_template('home.html')
    else:
        game_id = get_game_id(user_id)
        game = Game.query.filter_by(id=game_id).first()
        start = game.starttime
        print(time.strftime("%I %M %p",time.localtime(float(start))))
        return render_template('game.html', time = start)

def get_game_id(player_id):
    player = Player.query.filter_by(id=player_id).first()

    if player is not None:
        return player.game_id
    else:
        return None


