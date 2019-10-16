from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from forms import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = 'neco neco neco'
db = SQLAlchemy(app)
socketio = SocketIO(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return (self.user + "> " + self.message)


@app.route('/')
def index():
    if 'username' in session:
        return "logged in as {}".format(session['username'])
    return 'You are not logged in'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/chat', methods=('POST', 'GET'))
def chat():
    if 'username' in session:
        form = MessageForm()
        if form.validate_on_submit():
            message = Message(message=request.form['message'], user=session['username'])
            db.session.add(message)
            db.session.commit()
        messages = Message.query.all()
        return render_template("index.html", messages=messages, form=form, url = url_for('chat'))
    else:
        return "please, log in at /login"

@app.route('/login', methods=('POST', 'GET'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = request.form['username']
        session['username'] = user
        redirect(url_for('chat'))
    return render_template("login.html", form=form)


if __name__ == '__main__':
    socketio.run(app)
