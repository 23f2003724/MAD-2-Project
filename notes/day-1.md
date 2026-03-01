What i learned :- 
    today i setup the project. created the file strucure , setup the venv also write code on  app.py , extension.py , model.py also creted the database programmatically .. now the flask app is running 

Error i faced :- 
    1.) Circular import error 
        import app import db (models.py)
        import models (app.py)

    2.) spelling error :- 
        1.) app.config['SQLALCHEMY_DATABASE_URL'] ='sqlite:///database.db'
        2.) db.model
        3.) db.column

    3.)flask version error 
        @app.before_first_request
        def create_tables():
            db.create_all()

    4.) Didn't know the correct way to run app.py 

    5.) create two separate venv 

How i fixed it :-

    1.) created the separate file (extensions.py) 
            from flask_sqlalchemy import SQLAlchemy
            db = SQLAlchemy()
        then from extensions import db(app.py)
        also from extensions import db (models.py)

    2.) correct the spelling
        1.) app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
        2.) db.Model
        3.) db.Column

    3.) changed the code
        with app.app_context():
        db.create_all()

    4.) now i know , it should be run inside the correct folder.. in this case .. cd Backend .. python app.py 

    5.) deleted onw and again installed the all the required things in the another one 

