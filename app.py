from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mani/gitproject/flaskauth/artelus.db'
app.config['SECRET_KEY']='super-secret'
app.config['SECURITY_REGISTERABLE'] = True
db = SQLAlchemy(app)






roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# # Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='mani@gmail.com', password='mani')
#     db.session.commit()





# class User(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(120),unique=True)
#     email = db.Column(db.String(120),unique=True)
#     # password = db.Column(db.String(120),primary_key=True)

#     def __init__(self,username,email):
#         self.username = username
#         self.email = email
#     def __repr__(self):
#         return "<User %r>"%self.username





@login_required
@app.route('/')
def index():
    obj = User.query.all()
    return render_template('table.html',**locals())

@app.route('/home')
def home():

    data = "manikandan"
    return render_template('home.html',**locals())

@app.route('/post_user',methods=['POST'])
def post_user():
    user = User(request.form['username'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))








if __name__ == '__main__':
    app.run(debug=True)

