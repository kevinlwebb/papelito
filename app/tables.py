from app import db

class Player(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    enter = db.Column(db.String(10), nullable=False, default='0')

    game_id = db.Column(db.String(80), db.ForeignKey('game.id'),
        nullable=False)
    game = db.relationship('Game',
        backref=db.backref('players', lazy=True))

    def __repr__(self):
        return '<Player %r>' % self.name

class Character(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    game_id = db.Column(db.String(80), db.ForeignKey('game.id'),
        nullable=False)
    game = db.relationship('Game',
        backref=db.backref('characters', lazy=True))

    def __repr__(self):
        return '<Player %r>' % self.name

class Game(db.Model):
    id = db.Column(db.String(80), primary_key=True,  nullable=False)
    state = db.Column(db.String(20), nullable=False, default='0')
    starttime = db.Column(db.String(80), nullable=False, default='0')

    def __repr__(self):
        return '<Game %r>' % self.id