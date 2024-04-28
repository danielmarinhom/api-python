from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
import requests

from flask import Flask, render_template, request, redirect, url_for, session
from database import db, db_logs

from auth import login as lg
from auth import register as rg

app = Flask(__name__, template_folder='./')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'    #main db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_BINDS'] = {
    'logs': 'sqlite:///logs.db' 
}

key = 'testejwt-key'
app.config['JWT_SECRET_KEY'] = key
app.config['SECRET_KEY'] = key

jwt = JWTManager(app)

db.init_app(app)
#update db
with app.app_context():
    db.create_all()
    db.create_all(bind=['logs'])

def get_info():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    return username, email, password

#APPLICATION ROUTES
#INDEX
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#DASHBOARD (protected by jwt)
@jwt_required()
@app.route('/dashboard', methods=['GET'])
def dashboard():
    #erases these both values for security reasons, None is the return if access_token does not exist
    access_token = session.pop('access_token', None)
    username = session.pop('username', None)
    return render_template('dashboard.html', access_token=access_token, username=username)

#REGISTER
@app.route('/register', methods=['POST', 'GET'])
def register():
    if (request.method == 'POST'):
        username, email, password = get_info()
        if (rg(username, email, password)):
            return redirect(url_for('login')) 
        else:
            return redirect(url_for('index')) 
    elif (request.method == 'GET'):
        return render_template('register.html')
    
#LOGIN
@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username, email, password = get_info()
        access_token = lg(username, email, password)
        if(access_token):
            #defines these both variables in the session for being used by dashboard later and to avoid showing on url
            session['username'] = username
            session['access_token'] = access_token 
            user = Database(id=gen_id(), username=username, email=email, password=password)
            log = Log(id=gen_id(), event="register", id_user=user.id, timestamp=datetime.now())
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))
        
    elif (request.method == 'GET'):
        return render_template('login.html')
    
#LOGOUT
@app.route('/logout', methods=['POST'])
def logout():
    session['access_token'] = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)