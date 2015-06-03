#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

# TODO: 
# 1. fcn to make the tasklist from taskid
# 2. db interaction!
# 3. change to surveys, questions, answers

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# helper to make URIs for navigating API
def make_public_task(task):
	new_task = {}
	for field in task:
		if field == 'id':
			new_task['uri'] = url_for('get_task', task_id=task['id'],
							  _external=True)
		else:
			new_task[field] = task[field]
	return new_task

# index page
@app.route('/', methods = ['GET'])
def index():
    return "Hello, World!"

# get a list of tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

# get a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):	

	# check for tasks which match the task_id
	tasklist = []
	for task in tasks:
		if task['id'] == task_id:
			tasklist.append(task)
	
	# if you don't find any, return 404
	if len(tasklist) == 0:
		abort(404)

	# return first match
	return jsonify({'task': tasklist[0]})

# add new items to task database
@app.route('/tasks', methods=['POST'])
def create_task():
	# if not a json request, or request doesn't have title, return 400
	if not request.json or not 'title' in request.json:
		abort(400)
	
	# new task_id iterates latest task by 1
	task = {
		'id': tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	
	tasks.append(task)
	
	return jsonify({'task': task}), 201

# update items in database
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

	# check for tasks which match the task_id
	tasklist = []
	for task in tasks:
		if task['id'] == task_id:
			tasklist.append(task)

	if len(tasklist) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	if 'done' in request.json and type(request.json['done']) is not bool:
		abort(400)
	tasklist[0]['title'] = request.json.get('title', tasklist[0]['title'])
	tasklist[0]['description'] = request.json.get('description', tasklist[0]['description'])
	tasklist[0]['done'] = request.json.get('done', tasklist[0]['done'])
	return jsonify({'task': tasklist[0]})	

# delete items from database
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
	tasklist = []
	for task in tasks:
		if task['id'] == task_id:
			tasklist.append(task)
	if len(tasklist) == 0:
		abort(404)
	tasks.remove(tasklist[0])
	return jsonify({'result': True})

# error handlers
# 404 handler to keep API responses JSON (flask's default 404 is html)
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)