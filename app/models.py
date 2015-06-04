from app import db
import json

def to_dict(inst, cls):
    """
    Convert the sql alchemy query result to a dictionary.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d

class Survey(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index = True, unique = True)
	list_q = db.Column(db.String(255), index = True) 
	responses = db.relationship('Response', backref='parent', lazy='dynamic')
	
	def __repr__(self):
		return '<Survey %r>' % (self.name)

	@property
	def dict(self):
	    return to_dict(self, self.__class__)

class Response(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	time_created = db.Column(db.DateTime)
	id_surveys = db.Column(db.Integer, db.ForeignKey('survey.id'))
	answers = db.relationship('Answer', backref='r_answer', lazy = 'dynamic')

	def __repr__(self):
		return '<Response %r>' % (self.id)
		
	@property
	def dict(self):
	    return to_dict(self, self.__class__)

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text_q = db.Column(db.String(511))
	answers = db.relationship('Answer', backref='q_answer', lazy = 'dynamic')

	def __repr__(self):
		return '<Question %r>' % (self.text_q)

	@property
	def dict(self):
	    return to_dict(self, self.__class__)

class Answer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_questions = db.Column(db.Integer, db.ForeignKey('question.id'))
	id_responses = db.Column(db.Integer, db.ForeignKey('response.id'))
	text_a = db.Column(db.String(511))

	def __repr__(self):
		return '<Answer %r>' % (self.id)

	@property
	def dict(self):
	    return to_dict(self, self.__class__)
