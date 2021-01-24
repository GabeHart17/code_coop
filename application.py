import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager
from scripts.users import User, UserManager
# from scripts/database_manager import DatabaseManager, Challenge, TestCase

app = Flask(__name__)
app.secret_key = os.urandom(24)

# db_mgr = DatabaseManager(os.environ['DATABASE_URL'])
usr_mgr = UserManager(os.environ['DATABASE_URL'])
login_mgr = LoginManager()
login_mgr.init_app(app)

@login_mgr.user_loader
def load_user(uid):
    return usr_mgr.get_user_by_id(uid)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/challenge', methods=['GET'])
# def challenge():
#     id = request.args.get('c')
#     ch = dbmgr.get_challenge_by_id(id)
#     return render_template('challenge.html',
#         title=ch.title,
#         description=ch.description,
#         instructions=ch.instructions,
#         shown_tests=list(filter(lambda x: x.visible, ch.test_cases)),
#         hidden_tests=list(filter(lambda x: not x.visible, ch.test_cases)))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    uname = request.form['username']
    usr = usr_mgr.get_user_by_name(uname)
    err = ''
    if usr is not None:
        psk = request.form['password']
        if (usr_mgr.authenticate_user(usr, psk)):
            login_user(usr)
            return redirect('/index')
        else:
            err = 'invalid_credentials'
    else:
        err = 'no such user'
    return render_template('login.html', error=err)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    err = ''
    uname = request.form['username']
    psk0 = request.form['pasword']
    psk1 = request.form['confirmpassword']
    if ws.safe_str_cmp(psk0, psk1):
        if usr_mgr.create_user(uname, psk0):
            return redirect('login')
        else:
            err = 'username taken'
    else:
        err = 'passwords do not match'
    return render_template('register.html', error=err)

if __name__ == '__main__':
    app.run()
