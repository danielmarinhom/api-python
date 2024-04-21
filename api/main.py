from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__, template_folder='./')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return "<Task %r>" % self.id

with app.app_context():
    db.create_all()


def verify_data(username, email, password):
    query = Database.query.filter_by(username=username, email=email, password=password).first()
    return query is not None

#APPLICATION ROUTES
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/post_database', methods=['POST', 'GET'])
def post_database():
    if (request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        database = Database(username=username, email=email, password=password)
        db.session.add(database)
        db.session.commit()
        return redirect(url_for('dashboard'))
    
@app.route('/get_database', methods=['POST', 'GET'])
def get_database():
    if(request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if(verify_data(username, email, password)):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)