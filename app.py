
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}
rooms = {}

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect('/chat')
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    return render_template('chat.html', username=session['username'])

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f"{username} joined the room.", to=room)

@socketio.on('message')
def handle_message(data):
    send(data, to=data['room'])

@socketio.on('private_message')
def private_message(data):
    emit('private_message', data, to=data['to'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
