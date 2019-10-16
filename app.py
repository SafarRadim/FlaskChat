from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'neco neco neco'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.message

@app.route('/', methods=('POST', 'GET'))
def index():
    form = Form()
    if form.validate_on_submit():
        message = Message(message=request.form['message'])
        db.session.add(message)
        db.session.commit()
    messages = Message.query.all()
    return render_template("index.html", messages=messages, form=form)

@app.route('/add', methods=('POST', 'GET'))
def add():
    form = Form()
    if form.validate_on_submit():
        message = Message(message=request.form['message'])
        db.session.add(message)
        db.session.commit()
        return redirect("/")
    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run()
