from app import db
from app import app

class Survey(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), unique = True) # name of survey
	list_q = db.Column(db.String(255)) # list of questions in query
	responses = db.relationship ('Survey_Response', backref='parent', lazy='dynamic')
	
	def __repr__(self):
		return '<Survey %r>' % (self.name)


class Survey_Response(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_surveys = db.Column(db.Integer, db.ForeignKey('Survey.id')) # associated survey
	time_created = db.Column(db.DateTime) # when did we get this response
	
	def __repr__(self):
		return '<Survey Response %r>' % (self.id)


class Answer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_questions = db.Column(db.Integer, db.ForeignKey('Question.id')) # associated question
	id_survey_responses = db.Column(db.Integer, db.ForeignKey('Survey_Response.id')) # associated response
	text_a = db.Column(db.String(511))

	def __repr__(self):
		return '<Answer %r>' % (self.id)


class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text_q = db.Column(db.String(511))

	def __repr__(self):
		return '<Question %r>' % (self.text_q)