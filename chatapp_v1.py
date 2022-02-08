from flask import Flask, render_template

app = Flask(__name__)


chats = [
    {'username': 'user555', 'message': 'Hai, gimana kalo nanti malem ketemuan di ....'},
    {'username': 'user999', 'message': 'sip deh, ntar ak bawain ...'},
]

@app.route("/")
def chat():
    return render_template('chat_v1.html', chats=chats)