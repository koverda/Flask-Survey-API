from flask import render_template, jsonify, abort
from flask import make_response, request, url_for
from app import app, models, db


def validate_model_obj(model_obj, check_id):
	"""Validates that the model object exists with the specified id

	model_obj - model object to validate
	id - value of id we are trying to match for said object
	"""
	if model_obj.query.get(check_id) != None:
		return True # found matching id
	else:
		return False # no match

def refresh_model(model_obj):
	"""Update model data, returns it as a list of dictionaries

	model_obj - model object to update and return
	"""
	model_as_list = []
	model_ents = model_obj.query.all()
	for model_ent in model_ents:
		model_as_list.append(model_ent.dict)
	return model_as_list

def make_uri(thing, fcn_name):
	"""Make URIs for navigating API

	thing - what we want to make into a URI
	fcn_name - target endpoint of URI
	"""
	new_thing = {}
	for field in thing:
		if field == 'id':
			new_thing['uri'] = url_for(fcn_name, id=thing['id'], _external=True)
		else:
			new_thing[field] = thing[field]
	return new_thing

def match_id(check_list, check_id):
	"""Search list of dictionaries for entry that matches specified id

	check_list - list we are looking in
	check_id - id we are looking for 
	"""
	matches = []
	for item in check_list:
		if item['id'] == check_id:
			matches.append(item)
	return(matches)


# -------------------- Views --------------------

# index page
@app.route('/', methods = ['GET'])
def index():
	return "Hello, World!"
	# TODO: add root contents (surveys, questions, etc)
	# look at tables in db, pop em out as list/dict


# -------------------- GET All Items Routers --------------------
@app.route('/surveys/', methods=['GET'])
def get_surveys():
	surveys_as_list = refresh_model(models.Survey)
	return	jsonify({'surveys': [make_uri(survey, 'get_survey') for \
			survey in surveys_as_list]})

@app.route('/questions/', methods=['GET'])
def get_questions():
	questions_as_list = refresh_model(models.Question)
	return	jsonify({'questions': [make_uri(question, 'get_question') for \
			question in questions_as_list]})

@app.route('/responses/', methods=['GET'])
def get_responses():
	responses_as_list = refresh_model(models.Response)
	return	jsonify({'responses': [make_uri(response, 'get_response') for \
			response in responses_as_list]})

@app.route('/answers/', methods=['GET'])
def get_answers():
	answers_as_list = refresh_model(models.Answer)
	return	jsonify({'answers': [make_uri(answer, 'get_answer') for \
			answer in answers_as_list]})


# -------------------- GET Single Item Routers --------------------
@app.route('/surveys/<int:id>/', methods=['GET'])
def get_survey(id):
	
	# update from DB
	surveys_as_list = refresh_model(models.Survey)

	# check for surveys which match the id
	surveylist = match_id(surveys_as_list, id)
	
	# if you don't find any, return 404
	if len(surveylist) == 0:
		abort(404)

	# return first match
	return jsonify({'survey': surveylist[0]})

@app.route('/questions/<int:id>/', methods=['GET'])
def get_question(id):
	
	# update from DB
	questions_as_list = refresh_model(models.Question)

	# check for questions which match the id
	questionlist = match_id(questions_as_list, id)
	
	# if you don't find any, return 404
	if len(questionlist) == 0:
		abort(404)

	# return first match
	return jsonify({'question': questionlist[0]})

@app.route('/responses/<int:id>/', methods=['GET'])
def get_response(id):
	
	# update from DB
	responses_as_list = refresh_model(models.Response)

	# check for surveys which match the id
	responselist = match_id(responses_as_list, id)
	
	# if you don't find any, return 404
	if len(responselist) == 0:
		abort(404)

	# return first match
	return jsonify({'response': responselist[0]})

@app.route('/answers/<int:id>/', methods=['GET'])
def get_answer(id):
	
	# update from DB
	answers_as_list = refresh_model(models.Answer)

	# check for surveys which match the id
	answerlist = match_id(answers_as_list, id)
	
	# if you don't find any, return 404
	if len(answerlist) == 0:
		abort(404)

	# return first match
	return jsonify({'survey': answerlist[0]})


# -------------------- POST Routers --------------------
@app.route('/surveys/', methods=['POST'])
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

@app.route('/questions/', methods=['POST'])
def create_question():
	
	# if not a json request, or request doesn't have a question text, return 400
	if not request.json or not 'text_q' in request.json:
		abort(400)

	try:
		question = models.Question(text_q=str(request.json['text_q']))
		
		# add survey to db
		db.session.add(question)
		db.session.commit()
		
		#return survey you added and success code
		return jsonify({'task': question.dict}), 201

	except:
		abort(400)

@app.route('/responses/', methods=['POST'])
def create_response():
	
	# if not a json request, or request doesn't have related survey, return 400
	if not request.json or not 'id_surveys' in request.json:
		abort(400)

	try:
		response = models.Response(id_surveys=int(request.json['id_surveys']))

		if validate_model_obj(models.Survey, int(request.json['id_surveys'])) == False:
			print ('failed validate')
			abort(400)

		# add survey to db
		db.session.add(response)
		db.session.commit()
		
		#return survey you added and success code
		return jsonify({'task': response.dict}), 201

	except:
		print("error posting response")
		abort(400)

@app.route('/answers/', methods=['POST'])
def create_answer():
	
	# if not a json request, or doesn't have answer text 
	# or doesn't have a related survey response or related question
	# throw a 400 error
	if not request.json or not ('text_a' and 'id_questions' and 'id_responses')\
			in request.json:
		abort(400)

	try:
		answer = models.Answer(text_a=str(request.json['text_a']),
							   id_questions=int(request.json['id_questions']),
							   id_responses=int(request.json['id_responses']))
		
		# add survey to db
		db.session.add(answer)
		db.session.commit()
		
		#return survey you added and success code
		return jsonify({'task': answer.dict}), 201

	except:
		abort(400)


# -------------------- PUT Routers --------------------
@app.route('/surveys/<int:id>/', methods=['PUT'])
def update_survey(id):

	# check for surveys which match the id
	survey_to_update = models.Survey.query.filter_by(id=id).first()

	# validate request	
	if survey_to_update == None:
		abort(404)
	if not request.json:
		abort(400)
	if 'name' in request.json and type(request.json['name']) != unicode:
		abort(400)
	if 'list_q' in request.json and type(request.json['list_q']) != unicode:
		abort(400)

	# update db
	survey_to_update.name = request.json.get('name', survey_to_update.name)
	survey_to_update.list_q = request.json.get('list_q',survey_to_update.list_q)
	db.session.commit()

	return jsonify({'survey': survey_to_update.dict})

@app.route('/questions/<int:id>/', methods=['PUT'])
def update_question(id):

	# check for questions which match the id
	question_to_update = models.Question.query.filter_by(id=id).first()

	# validate request	
	if question_to_update == None:
		abort(404)
	if not request.json:
		abort(400)
	if 'text_q' in request.json and type(request.json['text_q']) != unicode:
		abort(400)

	# update db
	question_to_update.text_q = \
			request.json.get('text_q',question_to_update.text_q)
	db.session.commit()

	return jsonify({'question': question_to_update.dict})

@app.route('/responses/<int:id>/', methods=['PUT'])
def update_response(id):

	# check for requests which match the id
	response_to_update = models.Response.query.filter_by(id=id).first()

	# validate request	
	if response_to_update == None:
		abort(404)
	if not request.json:
		abort(400)
	if 'id_surveys' in request.json and \
			type(request.json['id_surveys']) != unicode:
		abort(400)


	# update db
	response_to_update.id_surveys = \
			request.json.get('id_surveys', response_to_update.name)
	db.session.commit()

	return jsonify({'response': response_to_update.dict})

@app.route('/answers/<int:id>/', methods=['PUT'])
def update_answer(id):

	# check for answers which match the answer_id
	answer_to_update = models.Answer.query.filter_by(id=id).first()

	# validate request	
	if answer_to_update == None:
		abort(404)
	if not request.json:
		abort(400)
	if 'text_a' in request.json and \
			type(request.json['text_a']) != unicode:
		abort(400)
	if 'id_questions' in request.json and \
			type(request.json['id_questions']) != unicode:
		abort(400)
	if 'id_responses' in request.json and \
			type(request.json['id_responses']) != unicode:
		abort(400)

	# update db
	answer_to_update.text_a = \
			request.json.get('text_a', answer_to_update.text_a)
	answer_to_update.id_questions = \
			request.json.get('id_questions',answer_to_update.id_questions)
	answer_to_update.id_responses = \
			request.json.get('id_responses',answer_to_update.id_responses)		
	db.session.commit()

	return jsonify({'answer': answer_to_update.dict})


# -------------------- DELETE Routers --------------------
@app.route('/surveys/<int:id>/', methods=['DELETE'])
def delete_survey(id):

	# finding survey
	survey_to_delete = models.Survey.query.filter_by(id=id).first()
	if survey_to_delete == None:
		abort(404)

	# deleting from db
	db.session.delete(survey_to_delete)
	db.session.commit()

	return jsonify({'result': True})

@app.route('/questions/<int:id>/', methods=['DELETE'])
def delete_question(id):

	# finding question
	question_to_delete = models.Question.query.filter_by(id=id).first()
	if question_to_delete == None:
		abort(404)

	# deleting from db
	db.session.delete(question_to_delete)
	db.session.commit()

	return jsonify({'result': True})

@app.route('/responses/<int:id>/', methods=['DELETE'])
def delete_response(id):

	# finding response
	response_to_delete = models.Response.query.filter_by(id=id).first()
	if response_to_delete == None:
		abort(404)

	# deleting from db
	db.session.delete(response_to_delete)
	db.session.commit()

	return jsonify({'result': True})

@app.route('/answers/<int:id>/', methods=['DELETE'])
def delete_answer(id):

	# finding answer
	answer_to_delete = models.Answer.query.filter_by(id=id).first()
	if answer_to_delete == None:
		abort(404)

	# deleting from db
	db.session.delete(answer_to_delete)
	db.session.commit()

	return jsonify({'result': True})		


# error handlers to keep API responses JSON (flask's default 404 is html)
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Bad Request'}), 400)
