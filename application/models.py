from __init__ import db

class Half(db.Model):
    __tablename__ = 'halves'

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(10))
    topping1 = db.Column(db.String(25))
    topping2 = db.Column(db.String(25))
    topping3 = db.Column(db.String(25))
    time_added = db.Column(db.DateTime)

    def __repr__(self):
        return "<Pizza half with {}, {}, and {}>".format(self.topping1, self.topping2, self.topping3)


# class Food(db.Model):
#     __tablename__ = 'foods'
    
#     id = db.Column(db.Integer, primary_key=True, index=True)


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    topping1_left = db.Column(db.String(25))
    topping2_left = db.Column(db.String(25))
    topping3_left = db.Column(db.String(25))
    topping1_right = db.Column(db.String(25))
    topping2_right = db.Column(db.String(25))
    topping3_right = db.Column(db.String(25))
    sauce = db.Column(db.String(25))
    size = db.Column(db.String(10))

    person1_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    person2_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    person1 = db.relationship('Person', foreign_keys=[person1_id])
    person2 = db.relationship('Person', foreign_keys=[person2_id])

    time_added = db.Column(db.DateTime)

    def __repr__(self):
        return "<{} pizza created at {}>".format(self.size.title(), self.time_added)


class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(50))
    location = db.Column(db.String(10))


class Topping(db.Model):
    __tablename__ = 'toppings'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(25), unique=True)


class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True, index=True)
    state = db.Column(db.String(20))
    food = db.Column(db.String(25))
    deadline = db.Column(db.DateTime)
    arrivalmin = db.Column(db.Integer)
    arrivalmax = db.Column(db.Integer)
    timer_id = db.Column(db.String(50))

    def __init__(self, state, food, deadline, arrivalmin, arrivalmax):
        self.state = state
        self.food = food
        self.deadline = deadline
        self.arrivalmin = arrivalmin
        self.arrivalmax = arrivalmax

    def __repr__(self):
        return "<state: {}, food: {}, deadline: {}, arriving in {} to {} minutes>".format(self.state, 
                                                                                          self.food, 
                                                                                          self.deadline, 
                                                                                          self.arrivalmin,
                                                                                          self.arrivalmax)


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(50), unique=True)
    time = db.Column(db.String(20))
