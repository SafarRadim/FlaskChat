from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import *

from gevent import monkey
from gevent.pywsgi import WSGIServer

from flask_socketio import SocketIO, send


monkey.patch_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = 'neco neco neco'
db = SQLAlchemy(app)
socketio = SocketIO(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return ((self.user_id.username, self.message))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    message = db.relationship("Message", backref="username", lazy = True)

    def __repr__(self):
        return(self.username)


@socketio.on('message')
def handle_message(message):
    print('recieved message: '+ message)
    LogUser = User.query.filter_by(username=session['username']).first()
    messageDb = Message(message=message, user_id=LogUser.id)
    db.session.add(messageDb)
    db.session.commit()
    send((session['username']+'> '+message), broadcast=True)


@app.route('/')
def index():
    user = None
    if 'username' in session:
        user = session['username']
    return render_template('index.html', user=user)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/chat', methods=('POST', 'GET'))
def chat():
    if 'username' in session:
        messages = Message.query.all()
        return render_template("chat.html", messages=messages)
    else:
        return "please, log in at /login"


@app.route('/login', methods=('POST', 'GET'))
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = request.form['username']
        password = request.form['password']
        userDb = User.query.filter_by(username=user).first()
        if userDb is not None:
            if password == userDb.password:
                session['username'] = user
                return redirect(url_for('chat'))
            else:
                error = "Bad Password"
        else:
            error = "Bad Login"
    return render_template("login.html", form=form, err=error)


@app.route('/register', methods=('POST', 'GET'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        newUser = User(username=request.form['username'], password=request.form['password'])
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


if __name__ == '__main__':
    socketio.run(app)
