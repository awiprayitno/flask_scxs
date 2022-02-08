from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as hasher

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def hash_password(self, password):
        self.password = hasher.hash(password)

    def verify_password(self, password):
        if self.password == password:
            self.hash_password(password)
            db.session.commit()
            return True
        else:
            try:
                return hasher.verify(password, self.password)
            except:
                return False

    def __repr__(self):
        return '<User %r>' % self.username

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), unique=True, nullable=False)
    dt = db.Column(db.Integer())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('chats', lazy=True))

    def __repr__(self):
        return '<Chat %r>' % self.id