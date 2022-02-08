from flask import Flask, render_template, request, url_for, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from models_v5 import *
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SECRET_KEY'] = '5117df0efd78d0ffd761b2d9348fc2889b71780bbd44d3b858314b10663f45ac'

db.init_app(app)
with app.app_context():
    db.create_all()

admin = Admin(app, name='Chat App', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Chat, db.session))

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

Bootstrap(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', type=str, default='')
    password = request.form.get('password', type=str, default='')

    if username and password:
        user = db.session.query(User).filter(User.username==username).first()
        if user and user.verify_password(password):
            login_user(user)
    
    return redirect(url_for('chat'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('chat'))

@app.route("/", methods=['GET', 'POST'])
def chat():
    app.logger.debug(f'request method: {request.method}')
    if request.method == 'POST' and current_user.is_authenticated:
        app.logger.debug(f'received post content: {request.form}')

        new_message = request.form.get('message')

        if new_message:
            new_chat = Chat(user=current_user, message=new_message, dt=int(time.time()))
            db.session.add(new_chat)
            db.session.commit()

    chats = db.session.query(Chat).order_by(Chat.id.asc())
    return render_template('chat_v6.html', chats=chats)