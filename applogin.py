from flask import Flask ,request,jsonify,abort,url_for,g,render_template,redirect
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
app.config['SECRET_KEY']='super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mani/gitproject/flaskauth/mani.db'
db = SQLAlchemy(app)

from flask_login import login_user,LoginManager,logout_user,login_required,logout_user
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()




##########

         #URL#
         #http://www.simplydjango.com/learn-python-efficiently/
         #https://blog.miguelgrinberg.com/post/restful-authentication-with-flask#
         #https://github.com/weinbergdavid/python-flask-security
         #http://docs.python-requests.org/en/master/
         #http://engineering.hackerearth.com/2014/08/21/python-requests-module/


############





class User(db.Model):
    __tablename__ = 'users'
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




login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # import ipdb;ipdb.set_trace()
    g.user = User.query.get(int(user_id))
    return User.query.get(int(user_id))













@app.route('/')
@login_required
def index():
    # import ipdb;ipdb.set_trace()
    print '-----------------------------',g.user.username
    obj = User.query.all()
    return render_template('table.html',**locals())






@app.route('/api/users', methods = ['POST'])
def new_user():
    # import ipdb;ipdb.set_trace()
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username })






@app.route('/login',methods=['POST','GET'])
def login():
    # import ipdb;ipdb.set_trace()
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return "Your Authentication failure"
        login_user(user)
        obj = User.query.all()
        return redirect(url_for('index'))
        # return render_template('table.html',**locals())
    if request.method == 'GET':
        return render_template('register.html',**locals())



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))













@app.route('/diabetic_retinopathy/predictions')
@auth.login_required
def get_resource():
    return jsonify({ "imagename": "orginal.jpg","taskstatus": "/diabetic_retinopathy/predictions/971857cb-a49e-4b27-9b3d-39002ba56fe8" })



@app.route('/diabetic_retinopathy/predictions/<task_id>')
@auth.login_required
def get_resources(task_id):
    return jsonify({"current": 100, "result": "No abnormality detected (0)", "state": "SUCCESS", "status": "orginal.jpg - DR Probabilities = [89.97%, 10.03%]", "total": 100})








@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True




# @app.route('/')
# @auth.login_required
# def index():
#     return "Hello World"

if __name__=='__main__':
    app.run(debug=True)