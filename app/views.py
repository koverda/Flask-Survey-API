from flask import render_template, jsonify, abort, make_response, request, url_for
from app import app, models

# database, for now
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

surveys = models.Survey.query.all()
surveys_as_list = []
for survey in surveys:
	surveys_as_list.append(survey.dict)

# helper to make URIs for navigating API
def make_uri(thing, fcn_name):
    new_thing = {}
    for field in thing:
        if field == 'id':
            new_thing['uri'] = url_for(fcn_name, id=thing['id'], _external=True)
        else:
            new_thing[field] = thing[field]
    return new_thing


# index page
@app.route('/', methods = ['GET'])
def index():
    return "Hello, World!"

# list of surveys
@app.route('/surveys', methods=['GET'])
def get_surveys():
	# return jsonify({'surveys': [survey.dict for survey in surveys]})
	return	jsonify({'surveys': [make_uri(survey, 'get_survey') for survey in surveys_as_list]})

# get a list of tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_uri(task,'get_task') for task in tasks]})

# get a specific task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):	

	# check for tasks which match the id
	tasklist = []
	for task in tasks:
		if task['id'] == id:
			tasklist.append(task)
	
	# if you don't find any, return 404
	if len(tasklist) == 0:
		abort(404)

	# return first match
	return jsonify({'task': tasklist[0]})

# get a survey
@app.route('/surveys/<int:id>', methods=['GET'])
def get_survey(id):
	# check for tasks which match the id
	surveylist = []
	for survey in surveys_as_list:
		if survey['id'] == id:
			surveylist.append(survey)
	
	# if you don't find any, return 404
	if len(surveylist) == 0:
		abort(404)

	# return first match
	return jsonify({'survey': surveylist[0]})


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
