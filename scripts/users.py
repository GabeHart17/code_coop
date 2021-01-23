import psycopg2

class UserManager:
    def __init__(self, db_url):
        self.conn = psycopg2.connect("dbname=codecoop_users user=postgres")
        self.cur = self.conn.cursor()

    def get_user_by_name(self, uname):
        cur.execute("SELECT * FROM users WHERE username=%s", (uname,))
        u = cur.fetchone()
        if u is None: return u
        return User(u[0], u[1])


class User:
    def __init__(self, uid, uname):
        self.uid = uid
        self.uname = uname;
        self.auth = False

    def is_authenticated(self):
        return self.auth

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uid
