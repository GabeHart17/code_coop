import psycopg2
import werkzeug.security as ws

class UserManager:
    def __init__(self, db_url):
        self.conn = psycopg2.connect("dbname=codecoop user=postgres password=postgres host=localhost")
        self.cur = self.conn.cursor()

    def get_user_by_name(self, uname):
        self.cur.execute("SELECT * FROM users WHERE username=%s", (uname,))
        u = self.cur.fetchone()
        if u is None: return u
        return User(u[0], u[1], hash=u[2])

    def get_user_by_id(self, uid):
        self.cur.execute("SELECT * FROM users WHERE id=%s", (uid,))
        u = self.cur.fetchone()
        if u is None: return u
        return User(u[0], u[1], hash=u[2])

    # returns true if user was successfully created, false if username taken
    def create_user(self, uname, psk):
        if self.get_user_by_name(uname) is not None:
            return False
        hash = ws.generate_password_hash(psk)
        self.cur.execute("INSERT INTO users (username, hash) VALUES (%s, %s)", (uname, hash))
        return True

    def authenticate_user(self, usr, psk):
        usr_info = self.get_user_by_name(usr.uname)
        usr.auth = ws.check_password_hash(usr.hash, psk)
        return usr.auth


class User:
    def __init__(self, uid, uname, hash=''):
        self.uid = str(uid)
        self.uname = uname
        self.hash = hash
        self.auth = False

    def is_authenticated(self):
        return self.auth

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid
