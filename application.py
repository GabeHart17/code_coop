import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import werkzeug.security as ws
from scripts.users import User, UserManager
from scripts.database_manager import DatabaseManager, Challenge, TestCase

app = Flask(__name__)
app.secret_key = os.urandom(24)

db_url = os.environ['DATABASE_URL']
usr_mgr = UserManager(db_url)
db_mgr = DatabaseManager(db_url)
login_mgr = LoginManager()
login_mgr.init_app(app)

@login_mgr.user_loader
def load_user(uid):
    return usr_mgr.get_user_by_id(uid)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render_template('login.html')
    uname = request.form['username']
    usr = usr_mgr.get_user_by_name(uname)
    err = ''
    if usr is not None:
        psk = request.form['password']
        if (usr_mgr.authenticate_user(usr, psk)):
            login_user(usr)
            return redirect('/')
        else:
            err = 'invalid_credentials'
    else:
        err = 'no such user'
    return render_template('login.html', error=err)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        return render_template('register.html')
    err = ''
    uname = request.form['username']
    psk0 = request.form['password']
    psk1 = request.form['confirmpassword']
    if ws.safe_str_cmp(psk0, psk1):
        if usr_mgr.create_user(uname, psk0):
            return redirect('login')
        else:
            err = 'username taken'
    else:
        err = 'passwords do not match'
    return render_template('register.html', error=err)

@app.route('/profile', methods=['GET'])
def profile():
    req_usr = request.args.get('u')
    usr = usr_mgr.get_user_by_name(req_usr)
    if usr is None:
        return redirect('/')
    if current_user.is_authenticated and req_usr == current_user.uname:
        return redirect('/dashboard')
    chals = db_mgr.get_challenges_by_user(usr.uid)
    return render_template('profile.html', uname=usr.uname, challenges=chals)

if __name__ == '__main__':
    app.run()
