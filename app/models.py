from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30), nullable = False)
    lname = db.Column(db.String(30), nullable = False)
    username = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(30), nullable = False)



class DiaryEntries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable = False)
    event = db.Column(db.Text)
    feeling = db.Column(db.Text)
    comments = db.Column(db.Text)
    summ = db.Column(db.String(1), nullable=False)
    private = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
  

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, nullable=False)
    user2 = db.Column(db.Integer, nullable=False)
