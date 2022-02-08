from flask import Flask, render_template, request
from models_v3 import *
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def chat():
    app.logger.debug(f'request method: {request.method}')
    if request.method == 'POST':
        app.logger.debug(f'received post content: {request.form}')

        username = request.form.get('username')
        new_message = request.form.get('message')

        if username and new_message:
            user = db.session.query(User).filter(User.username==username).first()
            if not user:
                user = User(username=username, password='')
                db.session.add(user)

            new_chat = Chat(user=user, message=new_message, dt=int(time.time()))
            db.session.add(new_chat)

            db.session.commit()

    chats = db.session.query(Chat).order_by(Chat.id.asc())
    return render_template('chat_v3.html', chats=chats)