import sqlite3

from flask import abort
from flask import Flask, flash, session, redirect, url_for, request
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'alksdjalskdjalskdj'
conn = sqlite3.connect("./instance/services.db")

users = [{'user': 'user', 'psw': 'psw'}]

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, title, price):
        self.title = title
        self.price = price

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/edit', methods=['POST','GET'])
def edit():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        service = Service(title=title, price=price)
        try:
            db.session.add(service)
            db.session.commit()
            flash("Услуга добавлена", category='succes')
        except:
            flash("Ошибка добавления услуги", category='error')
    return render_template("edit.html")

@app.route('/buys')
def news():
    items = Service.query.order_by(Service.title).all()
    return render_template("buys.html", data=items)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST' and {'user': request.form['username'], 'psw': request.form['psw']} in users:
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile'))
    else:
        flash("Ошибка входа", category='error')
    return render_template('login.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Добавить услугу':
            return redirect(url_for('edit'))
        elif request.form['submit_button'] == 'Выйти':
            session.clear()
            return redirect(url_for('login'))
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)
