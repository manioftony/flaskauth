from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_login import login_user,LoginManager
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config['SECRET_KEY']='super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mani/gitproject/flaskauth/karthik.db'
db = SQLAlchemy(app)



@app.route('/')
def index():
    return "fddghfdh"






class User(db.Model,UserMixin):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


@app.route('/register',methods=['POST','GET'])
def register():
    # import ipdb;ipdb.set_trace()
    if request.method == 'POST':
         # username = request.json.get('username')
         # password = request.json.get('password')
         username = request.form['username']
         password = request.form['password']
         user = User.query.filter_by(username = username).first()
         if not user or not user.verify_password(password):
            return False
         login_user(user)
         # return redirect(url_for('index'))
         return "successfully registered"
    if request.method == 'GET':
        return render_template('register.html',**locals())


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return session.query(User).filter(User.id == userid).first()
    except:
        return None



def usercreation():
    db.create_all()
    obj = User(username="mani")
    obj.hash_password("mani")
    db.session.add(obj)
    db.session.commit()



if __name__ == '__main__':
    app.run(debug=True)





