import time
from flask_script import Manager
from app import create_app, db

app = create_app()
manager = Manager(app)

@manager.command
def createdb():
    db.create_all()

@manager.command
def dropdb():
    db.drop_all()

if __name__ == "__main__":
    manager.run()
