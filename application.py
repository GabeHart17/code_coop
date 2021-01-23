import os
import psycopg2
from flask import Flask, render_template, request
from scripts/database_manager import DatabaseManager, Challenge, TestCase

app = Flask(__name__)

dbmgr = DatabaseManager(os.environ['DATABASE_URL'])

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


if __name__ == '__main__':
    app.run()
