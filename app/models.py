from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from math import log
from app import db, login_manager, app
from flask_login import UserMixin
from flask import url_for

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__   = 'user'
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(20), unique=True, nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic     = db.Column(db.String(20), nullable=False, default='default.jpg')
    password        = db.Column(db.String(60), nullable=False)
    created_on      = db.Column(db.DateTime, default=db.func.now())
    admin           = db.Column(db.Boolean, nullable=False, default=False)
    editor          = db.Column(db.Boolean, nullable=False, default=False)
    promoter        = db.Column(db.Boolean, nullable=False, default=False)
    confirmed       = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on    = db.Column(db.DateTime, nullable=True)

    submitted_bands = db.relationship('Band', back_populates='submitter') # many bands submitted by one user
    submitted_news  = db.relationship('News', back_populates='submitter')

    threads     = db.relationship('Thread', backref='user', lazy=True)
    
    events      = db.relationship('Event', backref='user', lazy=True)
    # comments    = db.relationship('Comment', backref='category', lazy=True)

    venue_id            = db.Column(db.Integer, db.ForeignKey('venue.id'))
    festival_id         = db.Column(db.Integer, db.ForeignKey('festival.id'))

    def __init__(self, username, email, password, confirmed):
        self.username       = username
        self.email          = email
        self.password       = password
        self.confirmed      = confirmed

    def get_reset_token(self, expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_pic}')"

class Band(db.Model):
    __tablename__   = 'band'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(120), unique=True, nullable=False)
    username        = db.Column(db.String(120), unique=True, nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    formed          = db.Column(db.Integer, nullable=False)
    is_active       = db.Column(db.String(60), nullable=False)
    genre           = db.Column(db.String(20), nullable=False)
    subgenre        = db.Column(db.String(20), nullable=False)
    lyrical_theme   = db.Column(db.String(20), nullable=False)

    website         = db.Column(db.String(120), nullable=True)
    twitter         = db.Column(db.String(120), nullable=True)
    facebook        = db.Column(db.String(120), nullable=True)
    instagram       = db.Column(db.String(120), nullable=True)
    bandcamp        = db.Column(db.String(120), nullable=True)

    city        = db.Column(db.String(20), nullable=False)
    province    = db.Column(db.String(2), nullable=False)
    country     = db.Column(db.String(60), nullable=False)

    submitted_on      = db.Column(db.DateTime, default=db.func.now())
    submitter_id      = db.Column(db.Integer, db.ForeignKey('user.id'))
    submitter         = db.relationship('User', back_populates='submitted_bands')

    news              = db.relationship('News', back_populates='band')

    logo            = db.Column(db.String(20), nullable=False, default='default.jpg')
    band_pic        = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Band('{self.name}', '{self.email}', '{self.formed}', '{self.genre}', '{self.city}', '{self.logo}', '{self.band_pic}')"

class Venue(db.Model):
    __tablename__   = 'venue'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(120), unique=True, nullable=False)
    username        = db.Column(db.String(120), unique=True, nullable=False)
    email           = db.Column(db.String(120), unique=True, nullable=False)
    founded         = db.Column(db.Integer, nullable=False)
    is_active       = db.Column(db.String(60), nullable=False)

    street_name     = db.Column(db.String(60), nullable=False)
    street_number   = db.Column(db.Integer, nullable=False)
    unit_number     = db.Column(db.Integer)
    city            = db.Column(db.String(20), nullable=False)
    postal_code     = db.Column(db.String(7), nullable=False)
    province        = db.Column(db.String(2), nullable=False)
    country         = db.Column(db.String(60), nullable=False)
    phone_number    = db.Column(db.Integer, nullable=False)
    capacity        = db.Column(db.Integer, nullable=False)

    website         = db.Column(db.String(120))
    twitter         = db.Column(db.String(120))
    facebook        = db.Column(db.String(120))
    instagram       = db.Column(db.String(120))

    venue_pic     = db.Column(db.String(20), nullable=False, default='default.jpg')

    news = db.relationship('News', back_populates='venue')

    def __repr__(self):
        return f"Venue('{self.name}', '{self.email}', '{self.founded}', '{self.street_address}', '{self.city}', '{self.venue_pic}')"

class Festival(db.Model):
    __tablename__ = 'festival'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), unique=True, nullable=False)
    username    = db.Column(db.String(120), unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    founded     = db.Column(db.Integer, nullable=False)
    is_active   = db.Column(db.String(60), nullable=False)

    date    = db.Column(db.DateTime)

    venue           = db.Column(db.String(60))
    street_name     = db.Column(db.String(60), nullable=False)
    street_number   = db.Column(db.Integer, nullable=False)
    unit_number     = db.Column(db.Integer)
    city            = db.Column(db.String(20), nullable=False)
    postal_code     = db.Column(db.String(7), nullable=False)
    province        = db.Column(db.String(2), nullable=False)
    country         = db.Column(db.String(60), nullable=False)
    phone_number    = db.Column(db.Integer, nullable=False)
    capacity        = db.Column(db.Integer, nullable=False)

    website         = db.Column(db.String(120))
    twitter         = db.Column(db.String(120))
    facebook        = db.Column(db.String(120))
    instagram       = db.Column(db.String(120))

    logo            = db.Column(db.String(20), nullable=False, default='default.jpg')
    festival_pic    = db.Column(db.String(20), nullable=False, default='default.jpg')
    grounds_map     = db.Column(db.String(20), nullable=False, default='default.jpg')

    news = db.relationship('News', back_populates='festival')


    def __repr__(self):
        return f"Festival('{self.name}', '{self.email}', '{self.founded}', '{self.street_address}', '{self.city}', '{self.logo}')"

class Event(db.Model):
    __tablename__   = 'event'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.String(120), nullable=False)
    location        = db.Column(db.String(120), nullable=False)
    date            = db.Column(db.DateTime, nullable=False)
    event_image     = db.Column(db.String(20), nullable=False, default='default.jpg')

    description     = db.Column(db.String(1000), nullable=False)
    start_time      = db.Column(db.DateTime, nullable=False)
    set_time        = db.Column(db.DateTime)

    band_id         = db.Column(db.Integer, db.ForeignKey('band.id'))
    attendee_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    venue_id        = db.Column(db.Integer, db.ForeignKey('venue.id'))
    # promoter_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    festival_id     = db.Column(db.Integer, db.ForeignKey('festival.id'))

class Ticket(db.Model):
    __tablename__   = 'ticket'
    id              = db.Column(db.Integer, primary_key=True)
    event_id        = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    festival_id     = db.Column(db.Integer, db.ForeignKey('festival.id'), nullable=False)
    owner_id        = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_name      = db.Column(db.String(120), nullable=False)
    date            = db.Column(db.DateTime, nullable=False)
    location        = db.Column(db.String(120), nullable=False)
    price           = db.Column(db.Integer, nullable=False)

    total_tickets       = db.Column(db.Integer, nullable=False)
    available_tickets   = db.Column(db.Integer, nullable=False)
    event_time          = db.Column(db.DateTime, nullable=False)
    band_id             = db.Column(db.Integer, db.ForeignKey('band.id'), nullable=False)
    event_image         = db.Column(db.String(20), nullable=False, default='default.jpg')

    # smart_contract      = 
    # qr_code_generator   =

class Thread(db.Model):
    __tablename__ = 'thread'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(250), nullable=False)
    text        = db.Column(db.String(5000), default=None)
    link        = db.Column(db.String(250), default=None)
    image       = db.Column(db.String(20), default=None)
    thumbnail   = db.Column(db.String(20), default=None)

    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
    band_id         = db.Column(db.Integer, db.ForeignKey('band.id'))
    venue_id        = db.Column(db.Integer, db.ForeignKey('venue.id'))
    festival_id        = db.Column(db.Integer, db.ForeignKey('festival.id'))
    event_id           = db.Column(db.Integer, db.ForeignKey('event.id'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return '<Thread %r>' % (self.title)

    def get_age(self):
        """
        returns the raw age of this thread in seconds
        """
        return (self.created_on - datetime.datetime(1970, 1, 1)).total_seconds()

    def pretty_date(self, typeof='created'):
        """
        returns a humanized version of the raw age of this thread,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        if typeof == 'created':
            return utils.pretty_date(self.created_on)
        elif typeof == 'updated':
            return utils.pretty_date(self.updated_on)

class News(db.Model):
    __tablename__ = 'news'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(500), nullable=False)
    title_url   = db.Column(db.String(500), nullable=False)
    text        = db.Column(db.String(5000), nullable=False)
    image       = db.Column(db.String(20), nullable=False, default='default.jpg')

    submitter_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    submitter        = db.relationship('User', back_populates='submitted_news')

    band_id         = db.Column(db.Integer, db.ForeignKey('band.id')) # make this able to tie to many bands
    band            = db.relationship('Band', back_populates='news')

    venue_id        = db.Column(db.Integer, db.ForeignKey('venue.id'))
    venue           = db.relationship('Venue', back_populates='news')

    festival_id     = db.Column(db.Integer, db.ForeignKey('festival.id'))
    festival        = db.relationship('Festival', back_populates='news')

    event_id        = db.Column(db.Integer, db.ForeignKey('event.id'))

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    # comments = db.relationship('Comment', backref='thread', lazy='dynamic')

    def __init__(self, title, text, submitter_id):
        self.title = title
        self.text = text
        self.submitter_id = submitter_id

    def __repr__(self):
        return '<Thread %r>' % (self.title)

    def get_age(self):
        """
        returns the raw age of this thread in seconds
        """
        return (self.created_on - datetime.datetime(1970, 1, 1)).total_seconds()

    def pretty_date(self, typeof='created_on'):
        """
        returns a humanized version of the raw age of this thread,
        eg: 34 minutes ago versus 2040 seconds ago.
        """
        if typeof == 'created_on':
            return utils.pretty_date(self.created_on)
        elif typeof == 'updated_on':
            return utils.pretty_date(self.updated_on)