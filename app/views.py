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

# pulling and formatting model data as needed
def refresh_model(model_obj):
	model_as_list = []
	model_ents = model_obj.query.all()
	for model_ent in model_ents:
		model_as_list.append(model_ent.dict)
	return model_as_list


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
@app.route('/surveys/', methods=['GET'])
@app.route('/surveys', methods=['GET'])
def get_surveys():
	surveys_as_list = refresh_model(models.Survey)
	return	jsonify({'surveys': [make_uri(survey, 'get_survey') for \
			survey in surveys_as_list]})

# list of questions
@app.route('/questions/', methods=['GET'])
@app.route('/questions', methods=['GET'])
def get_questions():
	questions_as_list = refresh_model(models.Question)
	return	jsonify({'questions': [make_uri(question, 'get_question') for \
			question in questions_as_list]})

# get a specific survey
@app.route('/surveys/<int:id>/', methods=['GET'])
@app.route('/surveys/<int:id>', methods=['GET'])
def get_survey(id):
	surveys_as_list = refresh_model(models.Survey)

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

# get a specific question
@app.route('/questions/<int:id>/', methods=['GET'])
@app.route('/questions/<int:id>', methods=['GET'])
def get_question(id):
	questions_as_list = refresh_model(models.Question)

	# check for tasks which match the id
	questionlist = []
	for question in questions_as_list:
		if question['id'] == id:
			questionlist.append(question)
	
	# if you don't find any, return 404
	if len(questionlist) == 0:
		abort(404)

	# return first match
	return jsonify({'question': questionlist[0]})

# add new survey
@app.route('/surveys/', methods=['POST'])
@app.route('/surveys', methods=['POST'])
def create_survey():
	# if not a json request, or request doesn't have name, return 400
	if not request.json or not 'name' in request.json:
		abort(400)
	try:
		survey = models.Survey(name=str(request.json['name']), 
							   list_q=str(request.json['list_q']))
		
		# add survey to db
		db.session.add(survey)
		db.session.commit()
		
		#return survey you added and success code
		return jsonify({'task': survey.dict}), 201
	except:
		abort(400)

# ------------- task stuff ------------

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
