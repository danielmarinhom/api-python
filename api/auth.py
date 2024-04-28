#from flask import session, redirect, url_for
from flask_jwt_extended import create_access_token
from database import Log, Database, db, db_logs
import random
from datetime import datetime

def verify_data(username, email, password):
    query = Database.query.filter_by(username=username, email=email, password=password).first()
    if(query is not None):
        if(query.is_admin):
            return 2
        else:
            return 1
    else:
        return 0

def login(username, email, password):
    if(verify_data(username, email, password) == 1):
        access_token = create_access_token(identity=username)
        user = Database.query.filter_by(username=username).first()
        log = Log(id=gen_id(), event="login", id_user=user.id, timestamp=datetime.now())
        post_log(log)
        return access_token
    else:
        return None
      
def gen_id():
    return random.randint(1, 999999) 

def register(username, email, password):
        user = Database(id=gen_id(), username=username, email=email, password=password)
        log = Log(id=gen_id(), event="register", id_user=user.id, timestamp=datetime.now())
        post_log(log)
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

def post_log(log):
    try:         
        db_logs.session.add(log)
        db_logs.session.commit() 
        return True
    except Exception as e:
        db_logs.session.rollback()
        return False
      