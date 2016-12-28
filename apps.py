from flask import Flask,render_template,request,redirect,url_for,g,jsonify,session
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_login import login_user,LoginManager,logout_user
from passlib.apps import custom_app_context as pwd_context
from uuid import uuid4
app = Flask(__name__)
app.config['SECRET_KEY']='super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mani/gitproject/flaskauth/karthik.db'
db = SQLAlchemy(app)







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



login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    g.user = User.query.get(int(user_id))
    return User.query.get(int(user_id))










@app.route('/')
@login_required
def index():
    # import ipdb;ipdb.set_trace()
    print '-----------------------------',g.user.username
    obj = User.query.all()
    return render_template('table.html',**locals())


from flask import flash
@app.route('/login',methods=['POST','GET','PUT'])
def login():
    # import ipdb;ipdb.set_trace()
    if request.method == 'POST':

        session['token'] =  uuid4().hex[:32]
        # username = request.json.get('username')
        # password = request.json.get('password')
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return "Your Authentication failure"
        login_user(user)
        obj = User.query.all()
        # flash("use loghin")
        # return render_template('table.html',**locals())
        return redirect(url_for('index'))
         # return "successfully registered"
    if request.method == 'GET':
        return render_template('register.html',**locals())
    if request.method == 'PUT':
        session['token'] =  uuid4().hex[:32]
        username = request.json.get('username')
        password = request.json.get('password')
        user = User.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return jsonify({'Error':'Your Authentication failure'})
        login_user(user)
        return jsonify({'Message':'successfully logged in','session':session['token']})


@app.route('/logout')
def logout():
    logout_user()
    session.pop('token', None)
    return redirect(url_for('login'))





@app.route('/home',methods=['POST'])
# @login_required
def home():
    # import ipdb;ipdb.set_trace()
    try:
        obj = User.query.all()
        return jsonify({'user':'successfully logged in'})
    except:
        return jsonify({'failure':'authenticate failure'})

@app.route('/homes')
def homes():

    return jsonify({'user':'successfully logged in'})







def usercreation():
    db.create_all()
    obj = User(username="mani")
    obj.hash_password("mani")
    db.session.add(obj)
    db.session.commit()



if __name__ == '__main__':
    app.run(debug=True)




