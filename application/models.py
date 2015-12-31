from application import db

class Half(db.Model):
    __tablename__ = 'halves'

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(10))
    topping1 = db.Column(db.String(25))
    topping2 = db.Column(db.String(25))
    topping3 = db.Column(db.String(25))

    def __repr__(self):
        return "<Pizza half with {}, {}, and {}>".format(self.topping1, self.topping2, self.topping3)


# class Food(db.Model):
#     __tablename__ = 'foods'
    
#     id = db.Column(db.Integer, primary_key=True, index=True)


# class Person(db.Model):
#     __tablename__ = 'people'
    
#     id = db.Column(db.Integer, primary_key=True, index=True)


# class Pizza(db.Model):
#     __tablename__ = 'pizzas'
    
#     id = db.Column(db.Integer, primary_key=True, index=True)


class Topping(db.Model):
    __tablename__ = 'toppings'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(25), unique=True)


class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True, index=True)
    setting = db.Column(db.String(20), unique=True)
    value = db.Column(db.String(20))

    def __repr__(self):
        return "<{} set to {}>".format(self.setting, self.value)