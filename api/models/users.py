from ..extensions import db
from datetime import datetime


# --------------------------------------------------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_link_history = db.relationship("Link", backref="user", lazy=True)


    # --------------------------------------------------------
    def __init__(self, username, password, email, first_name, last_name, reg_date):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.reg_date = reg_date

    def __repr__(self):
        return f'User< {self.username}>'

    # -----------------------------------
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # -----------------------------------
    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    

    # ------------------------------------
