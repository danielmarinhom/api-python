from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
import requests

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__, template_folder='./')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'

key = 'testejwt-key'

app.config['JWT_SECRET_KEY'] = key
app.config['SECRET_KEY'] = key

jwt = JWTManager(app)
db = SQLAlchemy(app)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    #legible representation of database
    def __repr__(self):
        return "<Task %r>" % self.id

#update db
with app.app_context():
    db.create_all()


def verify_data(username, email, password):
    query = Database.query.filter_by(username=username, email=email, password=password).first()
    return query is not None

#APPLICATION ROUTES
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@jwt_required()
@app.route('/dashboard', methods=['GET'])
def dashboard():
    #acess_token = request.args.get('acess_token')
    #username = request.args.get('username')

    #erases these both values for security reasons, None is the return if access_token does not exist
    access_token = session.pop('access_token', None)
    username = session.pop('username', None)
    return render_template('dashboard.html', access_token=access_token, username=username)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if (request.method == 'POST'):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        database = Database(username=username, email=email, password=password)
        db.session.add(database)
        db.session.commit()
        return redirect(url_for('index'))
    elif (request.method == 'GET'):
        return render_template('register.html')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username= request.form['username']
        email = request.form['email']
        password = request.form['password']
        if(username == '' or email == '' or password == ''):
            return redirect(url_for('index'))
        if(verify_data(username, email, password)):
            access_token = create_access_token(identity=username)
            headers = {'Authorization': 'Bearer ' + access_token}
            response = requests.get('http://localhost:5000/dashboard', headers=headers)
            if(response.status_code == 200): 
                #defines these both variables in the session for being used by dashboard later and to avoid showing on url
                session['username'] = username
                session['access_token'] = access_token 
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    elif (request.method == 'GET'):
        return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session['access_token'] = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)