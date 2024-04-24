from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
import requests

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__, template_folder='./')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['JWT_SECRET_KEY'] = 'testejwt-key'
jwt = JWTManager(app)
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

@jwt_required()
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
        return redirect(url_for('index'))
    
@app.route('/get_database', methods=['POST', 'GET'])
def get_database():
    if(request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if(verify_data(username, email, password)):
            access_token = create_access_token(identity=username)
            headers = {'Authorization': 'Bearer ' + access_token}
            response = requests.get('http://localhost:5000/dashboard', headers=headers)
            if(response.status_code == 200): 
                return redirect(url_for('dashboard', access_token=access_token))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)