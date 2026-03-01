What i learned :- 
    - Build login (login.html, /login ,/admin, )
    - Build session system
    - Restrict routes based on role

Error i faced :- 
    1.) how to start venv again ?

    2.) login and admin both routes are not opening
 

How i fixed it :-

    1.) .\venv\Scripts\Activate

    2.) - user and User(db) was different .. spelling error 
        - from models import User
        - i was running without saving so again and again old app.py is running 