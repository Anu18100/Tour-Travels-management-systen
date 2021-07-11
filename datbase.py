from managment import db , login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    first = db.Column(db.String(20) , nullable = False)
    middle = db.Column(db.String(20) , nullable = False)
    last = db.Column(db.String(20) , nullable = False)
    email = db.Column(db.String(120) , unique = True , nullable = False)
    image_file = db.Column(db.String(20) , nullable = False , default = 'default.jpg')
    user_type = db.Column(db.String(20) , nullable = False)
    add1 = db.Column(db.String(20))
    add2 = db.Column(db.String(20))
    add3 = db.Column(db.String(20))
    add4 = db.Column(db.String(20))
    state = db.Column(db.String(20))
    city = db.Column(db.String(20))
    pincode = db.Column(db.Integer)
    password = db.Column(db.String(60) , nullable = False)
    tour = db.relationship('Tour' , backref='traveler',lazy=True)
    review = db.relationship('Review' , backref = 'rv' , lazy = True)
    def __repr__(self):
        return f"User({self.first} , {self.middle} , {self.last} , {self.email} ,{self.image_file})"



class Tour(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    place=db.Column(db.String(20) , nullable=False)
    doj=db.Column(db.DateTime , nullable=False)
    nop = db.Column(db.Integer , nullable=False , default=1)
    package_amt = db.Column(db.Integer , nullable= False)
    total_amt = db.Column(db.Integer , nullable=False)
    traveler_id = db.Column(db.Integer , db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User({self.place} , {self.doj} , {self.nop})"

class Buses(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    driver_name = db.Column(db.String(20) , nullable= False)
    contact = db.Column(db.Integer , nullable= False)
    status = db.Column(db.String(10) , nullable = False)

    def __repr__(self):
        return f"Buses({self.id} , {self.driver_name} , {self.contact} , {self.status})"


class Packages(db.Model):
    packages_id = db.Column(db.Integer , primary_key=True)
    destination = db.Column(db.String(50) , nullable= False)
    duration = db.Column(db.String(30) , nullable = False)
    amt = db.Column(db.Integer ,nullable = False)
    

    def __repr__(self):
        return f"Buses({self.packages_id} , {self.destination} , {self.duration} , {self.amt})"


class Review(db.Model):
    id =  db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(100) , nullable= False)
    date_review = db.Column(db.DateTime , nullable= False , default = datetime.utcnow)
    review = db.Column(db.Text , nullable= False)
    rver = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)

    def __repr__(self):
        return f"Review({self.title} , {self.date_review} , {self.review})"