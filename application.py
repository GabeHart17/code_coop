import os
import psycopg2
from flask import Flask, render_template, request
from scripts/database_manager import DatabaseManager, Challenge, TestCase
import werkzeug.security as ws

app = Flask(__name__)

db_mgr = DatabaseManager(os.environ['DATABASE_URL'])
usr_mgr = UserManager(os.environ['DATABASE_URL'])
login_mgr = LoginManager()
login_mgr.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/challenge', methods=['GET'])
def challenge():
    id = request.args.get('c')
    ch = dbmgr.get_challenge_by_id(id)
    return render_template('challenge.html',
        title=ch.title,
        description=ch.description,
        instructions=ch.instructions,
        shown_tests=list(filter(lambda x: x.visible, ch.test_cases)),
        hidden_tests=list(filter(lambda x: !x.visible, ch.test_cases)))

@app.route('/login', methods=['GET', 'POST'])
def login():
    uname = request.form['username']
    psk = request.form['password']
    p_hash = ws.generate_password_hash(psk)
    # get usr



if __name__ == '__main__':
    app.run()
