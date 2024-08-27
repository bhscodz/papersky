import os,random
from flask import jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user
from google.oauth2 import credentials
from google_auth_oauthlib import flow
from flask_migrate import Migrate
from flask import Flask,render_template,request,flash,redirect,url_for,g,send_from_directory
UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'*'}
migrate=Migrate()


Flows=flow.Flow.from_client_secrets_file(
   os.path.join(os.getcwd()+r'\secreats\clien_secreat.json'),
    scopes=[
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email', 
        'openid'],
        redirect_uri='http://localhost:5000/callback'
)

def random_str():
    l='abcdefghijklmnopqrstuvwxyz'
    s=''
    for i in range(1,11):
        s+=l[random.randint(1,25)]
    return s

def create_app(test_config=None):
    # creating and configuring the app
    app = Flask(__name__, instance_relative_config=True)


    app.config.from_mapping(
        SECRET_KEY='secreateisthebiggestnews',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    '''
    app.config['SQLALCHEMY_DATABASE_URI']=os.path.join(os.getcwd(), 'flaskr.sqlite')
    db=SQLAlchemy()
    migrate = Migrate()
    login_manager=LoginManager()
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
'''
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home():
        flash('hello new user','success')
        return render_template('index.html',name={'user':'shiv'} ,files=os.listdir('files/')) 
    
    @app.route('/login')
    def login_user_fr():
        pass

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
    
    return app



