from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__, template_folder='./')

@app.route('/', methods=['GET'])
def index():
    print ("type(password)")
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        if(verify_password(username, password)):
            return redirect(url_for('dashboard'))
        else:
            return "0"
        

def verify_password(username, password):
    file = pd.read_csv('passwords.csv')
    password = str(password)
    username = str(username)
    for index, row in file.iterrows():
        if (row['usernames'] == username) and (row['passwords'] == password):
            print (type(password))
    return False

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run(debug=True)