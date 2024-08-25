import os,random
from werkzeug.utils import secure_filename
import datetime
from flask import Flask,render_template,request,flash,redirect,url_for,g,send_from_directory
UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'*'}
def random_str():
    l='abcdefghijklmnopqrstuvwxyz'
    s=''
    for i in range(1,11):
        s+=l[random.randint(1,25)]
    return s
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        flash('hello','success')
        return render_template('index.html',name={'user':'shiv'} ,files=os.listdir('files/')) 
    
    @app.route('/upload',methods=['GET','POST'])
    def upload():
        print(request.method)
        if request.method == 'POST':
            print(request.args)
            if 'file' not in request.files:
                flash('No file part','error')
                print(1)
                return redirect('/')
            file = request.files['file']
            if file.filename == '':
                flash('No selected file','error')
                print(2)
                return render_template('failed.html')
            if file:
                print(3)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_str()+file.filename)
                file.save(file_path)
                flash('File successfully uploaded')
                return redirect(url_for('home'))
        return redirect(url_for('home'))
    
    @app.route('/myuploads/<filename>')
    def myuploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    
    return app



