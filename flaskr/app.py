import os,random
import flask
from flask import jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,login_manager,current_user
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from flask_migrate import Migrate
from flask import Flask,render_template,request,flash,redirect,url_for,g,send_from_directory

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'*'}
migrate=Migrate()
scopes=['https://www.googleapis.com/auth/userinfo.profile',
'https://www.googleapis.com/auth/userinfo.email', 
'openid']

# createing global flow to use everywhere
flow=Flow.from_client_secrets_file(
   os.path.join(os.getcwd()+r'\secreats\clien_secreat.json'),
   scopes,
   redirect_uri='http://localhost:5000/callback'
)

def random_str():
    l='abcdefghijklmnopqrstuvwxyz'
    s=''
    for i in range(1,11):
        s+=l[random.randint(1,25)]
    return s

app = Flask(__name__, instance_relative_config=True)

app.secret_key='mysecretekey'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app)
login_manager=LoginManager()
login_manager.init_app(app)
class User(UserMixin,db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(250),unique=True,nullable=False)
    password=db.Column(db.String(250),nullable=False)
    def __repr__(self):
            return self.username
#user login call back
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def home():
    flash('hello new user','success')
    return render_template('index.html',name={'user':'shiv'} ,files=os.listdir('files/')) 

@app.route('/authorize')
def login_user_fr():
    if 'credentials' not in flask.session: 
        authorization_url ,state=flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
        )
        flask.session['state']=state
        return redirect(authorization_url)
    else:
        return 'already authorized',200

@app.route('/callback')
def callback():
    state=flask.session['state']
    response=request.url
    flow.fetch_token(authorization_response=response)
    credentials=flow.credentials
    flask.session['credentials']=credentials
    print(credentials.token)

@app.route('/upload',methods=['GET','POST'])
def upload():
    print(request.method)
    if request.method == 'POST':
        print(request.args)
        if 'file' not in request.files:
            print(1)
            return jsonify({'status':'error','data':'no file selected'}),401
        files = request.files.getlist('file')
        for file in files:
            if file.filename == '':
                print(2)
                break
            if file:
                print(3)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_str()+file.filename)
                file.save(file_path)
        else:
            return jsonify({'status':'success','data':'voila! your files has been uploaded'}),200
    return jsonify({'status':'error','data':'file upload unsuccessfull'}),404

@app.route('/sendfiles',methods=['POST'])
def sendfiles():
    if request.method=='POST':
        data=request.json()
        print(data['username'])
        print(data['number'])
        print(data['t'])
        return 

    else:
        return 'bad request',400
        
@app.route('/myuploads/<filename>')
def myuploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)





