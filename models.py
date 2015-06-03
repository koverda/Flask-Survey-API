from app import db

class Survey(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index = True, unique = True)
	list_q = db.Column(db.String(255), index = True) 
	responses = db.relationship('Response', backref='parent', lazy='dynamic')
	
	def __repr__(self):
		return '<Survey %r>' % (self.name)

class Response(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	time_created = db.Column(db.DateTime)
	id_surveys = db.Column(db.Integer, db.ForeignKey('survey.id'))
	answers = db.relationship('Answer', backref='r_answer', lazy = 'dynamic')

	def __repr__(self):
		return '<Response %r>' % (self.id)

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text_q = db.Column(db.String(511))
	answers = db.relationship('Answer', backref='q_answer', lazy = 'dynamic')

	def __repr__(self):
		return '<Question %r>' % (self.text_q)

class Answer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_questions = db.Column(db.Integer, db.ForeignKey('question.id'))
	id_responses = db.Column(db.Integer, db.ForeignKey('response.id'))
	text_a = db.Column(db.String(511))

	def __repr__(self):
		return '<Answer %r>' % (self.id)
