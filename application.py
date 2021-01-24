import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, abort
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

@app.route('/browse', methods=['GET'])  # temporary
def browse():
    usrs = usr_mgr.all_usernames()
    return render_template('browse.html', users=usrs)

@app.route('/profile', methods=['GET'])
def profile():
    req_usr = request.args.get('u')
    if req_usr is None:
        return redirect('/')
    usr = usr_mgr.get_user_by_name(req_usr)
    if usr is None:
        return redirect('/')
    if current_user.is_authenticated and req_usr == current_user.uname:
        return redirect('/dashboard')
    chals = db_mgr.get_challenges_by_user(usr.uid)
    return render_template('profile.html', uname=usr.uname, challenges=chals)

@app.route('/challenge', methods=['GET'])
def challenge():
    req_ch = request.args.get('c')
    if req_ch is None:
        return redirect('/')
    ch = db_mgr.get_challenge_by_id(req_ch)
    if ch  is None:
        return redirect('/')
    auth = usr_mgr.get_user_by_id(ch.author_id).uname
    test_in = str([int(i.specified_input) for i in ch.test_cases])
    test_out = str([int(i.specified_output) for i in ch.test_cases])
    return render_template('challenge.html', challenge=ch, author=auth, ti=test_in, to=test_out)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    chals = db_mgr.get_challenges_by_user(current_user.uid)
    return render_template('dashboard.html', uname=current_user.uname, challenges=chals)

@app.route('/edit', methods=['GET'])
@login_required
def edit():
    ch_req = request.args.get('c')
    ch = Challenge(-1, current_user.uid, '', '', '', [])
    if ch_req is not None:
        ch = db_mgr.get_challenge_by_id()
    if ch.author_id != current_user.uid:
        return redirect('/dashboard')
    return render_template('editor.html', challenge=ch)

@app.route('/editorsave', methods=['POST'])
@login_required
def save_challenge():
    abort(501)
    # if request.form['cid'] >= 0:
    #     ch = db_mgr.get_challenge_by_id(request.form['cid'])
    #     if ch.author_id != current_user.uid:
    #         abort(401)
    #     if ch is not None:  # for future, fix so it actually updates rather than replaces
    #         db_mgr.delete_challenge(ch.cid)
    # test_cases = []
    # for i in range(1, 6):
    #     tc = TestCase(-1, not reqest.form[f'hid{i}'], request.form[f'tc{i}'], reqest.form[f'out{i}'])
    #     test_case.append(tc)
    # new_ch = Challenge(-1,
    #     current_user.uid,
    #     request.form['title'],
    #     request.form['desc'],
    #     request.form['instructions'],
    #     test_cases
    #     )
    # db_mgr.add_challenge(new_ch)
    # return redirect('/dashboard')

if __name__ == '__main__':
    app.run()
