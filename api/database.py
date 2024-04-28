from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_logs = SQLAlchemy()

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    #legible representation of database
    def __repr__(self):
        return "<Task %r>" % self.id

class Log(db_logs.Model):
    __bind_key__ = 'logs'
    id = db_logs.Column(db_logs.Integer, primary_key=True, autoincrement=True)
    event = db_logs.Column(db_logs.String(30))
    id_user = db_logs.Column(db_logs.Integer, db.ForeignKey('database.id')) #foreign key
    timestamp = db_logs.Column(db_logs.DateTime, nullable=False)
    #legible representation of database
    def __repr__(self):
        return "<Task %r>" % self.id