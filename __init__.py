# TODO: 
# 1. fcn to make the tasklist from taskid
# 2. db interaction!
# 3. change to surveys, questions, answers

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

# if __name__ == '__main__':
#     app.run(debug=True)