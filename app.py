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
            LogUser = User.query.filter_by(username=session['username']).first()
            message = Message(message=request.form['message'], user_id=LogUser.id)
            db.session.add(message)
            db.session.commit()
        messages = Message.query.all()
        return render_template("index.html", messages=messages, form=form, url = url_for('chat'), logged = session['username'])
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
                redirect(url_for('chat'))
            else:
                error = "Bad Login"
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
        return "registered"
    return render_template("register.html", form=form)


if __name__ == '__main__':
    socketio.run(app)
