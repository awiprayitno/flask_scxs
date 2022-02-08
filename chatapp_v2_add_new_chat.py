from flask import Flask, render_template, request

app = Flask(__name__)


chats = [
    {'username': 'user555', 'message': 'Hai, gimana kalo nanti malem ketemuan di ....'},
    {'username': 'user999', 'message': 'sip deh, ntar ak bawain ...'},
]

@app.route("/", methods=['GET', 'POST'])
def chat():
    app.logger.debug(f'request method: {request.method}')
    if request.method == 'POST':
        app.logger.debug(f'received post content: {request.form}')
        chats.append({
            'username': request.form.get('username'), 
            'message': request.form.get('message'), 
        })
    return render_template('chat_v2.html', chats=chats)