import os,random
import flask,requests
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

scopes=['https://www.googleapis.com/auth/userinfo.profile',
'https://www.googleapis.com/auth/userinfo.email', 
'openid']

# createing global flow to use everywhere
flow=Flow.from_client_secrets_file(
   os.path.join(os.getcwd()+r'\secreats\clien_secreat.json'),
   scopes,
   redirect_uri='http://localhost:5000/callback'
)

def random_str(long=False):
    if not long:
        l='abcdefghijklmnopqrstuvwxyz'
        s=''
        for i in range(1,11):
            s+=l[random.randint(1,25)]
        return s
    else:
        l='abcdefghijklmnopqrstuvwxyz'
        s=''
        for i in range(1,20):
            s+=l[random.randint(1,25)]
        return s

app = Flask(__name__, instance_relative_config=True)

app.secret_key='mysecretekey'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)

migrate = Migrate(app,db,render_as_batch=True)
login_manager=LoginManager()
login_manager.init_app(app)
class User(UserMixin,db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(250),unique=True,nullable=False)
    password=db.Column(db.String(250),nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    def __repr__(self):
            return self.username
#user login call back
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    if not current_user.is_authenticated:
        message='hello new user please login'
    else:
        message=f'hello {current_user.username}'
    flash('hello new user','success')
    return render_template('index.html',name={'user':'shiv'} ,message=message,files=os.listdir('files/')) 

@app.route('/authorize')
def authorize():
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
    state=flask.session.get('state')
    response=request.url
    flow.state=state
    flow.fetch_token(authorization_response=response)
    credentials=flow.credentials
    flask.session['credentials']=credentials_to_dict(credentials)
    print(credentials.token)
    response_b=login_the_user(credentials)
    return response_b


def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def login_the_user(credentials):
    response=requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization':f'Bearer {credentials.token}'}
    )
    if response.status_code==200:
        response=response.json()
        user =User.query.filter_by(email=response['email']).first()
        if not user:
            user=User(email=response['email'],username=response['name'],password=random_str(True))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return render_template('new_user.html')
        else:
            login_user(user)
            return render_template('new_user.html')
    else:
        return 'unable to sign in '
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('revoke_clear'))

@app.route('/revoke_clear')
def revoke_clear():
    credentials=flask.session.get('credentials')
    rev_req=requests.post(
    'https://oauth2.googleapis.com/revoke',
      params={'token': credentials['token']},
      headers = {'content-type': 'application/x-www-form-urlencoded'}
    )
    if rev_req.status_code==200:
        message='token revoked'
    else:
        message='an error occurred'
    try:
        if 'credentials' in flask.session:
            del flask.session['credentials']
            message+='cred session deleted'
    except:
        message+='cred cant be deleted'
    return render_template('logout.html',message=message)

@app.route('/myuploads/<filename>')
def myuploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)





