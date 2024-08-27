def deploy():
    from . import create_app,db
    from flask_migrate import upgrade,init,stamp,migrate
    from models import user
    
    app=create_app()
    app.app_context().push()
    db.create_all()

    init()
    stamp()
    migrate()
    upgrade()
deploy()