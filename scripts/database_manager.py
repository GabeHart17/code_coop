import psycopg2
import os

class DatabaseManager:
    def __init__(self, db_url):
        if 'FLASK_APP' in os.environ.keys():  # test if running locally
            self.conn = psycopg2.connect("dbname=codecoop user=postgres password=postgres host=localhost")
        else:
            self.conn = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.conn.cursor()

    def add_testcase(self, chal_id, test_case):
        self.cur.execute("INSERT INTO test_cases (challenge_id, shown, input, output) VALUES (%s, %s, %s, %s);",
        (chal_id, test_case.shown, test_case.specified_input, test_case.specified_output))
        conn.commit()
    def delete_testcase(self, case_id):
        self.cur.execute("DELETE FROM test_cases WHERE id=%s;", (case_id,))
        conn.commit()
    def update_testcase(self, case):
        self.cur.execute("UPDATE test_cases SET shown=%s, input=%s, output=%s WHERE id=%s;",
        (case.shown, case.specified_input, case.specified_output, case.case_id))
        conn.commit()
    def get_testcase_by_id(self, case_id):
        self.cur.execute("SELECT * FROM test_cases WHERE id=%s;", (case_id,))
        case_data = self.cur.fetchone()
        if case_data != None:
            case = list(case_data)
            return TestCase(*tuple(case[:1]+case[2:]))
        return None
    def add_challenge(self, chal):
        self.cur.execute("INSERT INTO challenges (title, author_id, description, instructions) VALUES (%s, %s, %s, %s);",
        (chal.title, chal.author_id, chal.desc, chal.instructions))
        self.cur.execute("SELECT MAX(id) FROM challenges;")
        chal.cid = self.cur.fetchone()[0]
        for case in chal.test_cases:
            self.add_testcase(chal.cid, case)
        conn.commit()
    def delete_challenge(self, chal_id):
        self.cur.execute("DELETE FROM challenges WHERE id=%s;", (chal_id,))
        self.cur.execute("DELETE FROM test_cases WHERE challenge_id=%s;", (chal_id,))
        conn.commit()
    def update_challenge(self, chal): #may not be a great method to call
        self.cur.execute("UPDATE challenges SET title=%s, author_id=%s, description=%s, instructions=%s WHERE id=%s;",
        (chal.title, chal.author_id, chal.desc, chal.instructions, chal.cid))
        self.cur.execute("SELECT * FROM test_cases WHERE challenge_id=%s;", (chal.cid,))
        db_data = cur.fetchall()
        chal_case_ids = [x.case_id for x in chal.test_cases]
        db_case_ids = [x[1] for x in db_data]

        for case_id in db_case_ids: #delete removed cases
            if case_id not in chal_case_ids:
                self.delete_testcase(case_id)
        for i in range(0, len(chal_case_ids)): # add new cases
            if chal_case_ids[i] not in db_case_ids:
                self.add_testcase(chal.cid, chal.test_cases[i])
            else:
                self.update_testcase(chal.test_cases[i])
        conn.commit()
    def get_challenge_by_id(self, chal_id):
        self.cur.execute("SELECT * FROM challenges WHERE id=%s;", (chal_id,))
        chal_data = self.cur.fetchone()
        if chal_data != None:
            chal_data = list(chal_data) + [[]]
            self.cur.execute("SELECT * FROM test_cases WHERE challenge_id=%s;", (chal_id,))
            test_cases = [list(x) for x in list(self.cur.fetchall())]
            for case in test_cases:
                chal_data[-1].append(TestCase(*tuple(case[:1]+case[2:])))
            return Challenge(*tuple(chal_data))
        return None
    def get_challenges_by_user(self, user_id):
        self.cur.execute("SELECT * FROM challenges WHERE author_id=%s;", (user_id,))
        chals = self.cur.fetchall()
        out = []
        for c in chals:
            out.append(Challenge(*c))
        return out
    def get_challenges_by_keywords(self, search_term):
        pass

class Challenge:
    def __init__(self, chal_id, author_id, title, desc, instructions, test_cases=[]):
        self.cid = chal_id
        self.title = title
        self.author_id = author_id
        self.desc = desc
        self.instructions = instructions
        self.test_cases = test_cases
    def new_test_case(self, shown, specified_input, specified_output):
        self.test_cases.append(TestCase(-1, shown, specified_input, specified_output))

class TestCase:
    def __init__(self, case_id, shown, specified_input, specified_output):
        self.case_id = case_id
        self.shown = shown
        self.specified_input = specified_input
        self.specified_output = specified_output

if __name__ == "__main__":
    conn = psycopg2.connect("dbname=mydb user=benjabob317")
    manager = DatabaseManager(conn)

    factorial = Challenge(
        -1,
        "Factorial",
        0,
        "For a given integer n return n(n-1)(n-2)...*1",
        "Make a function that finds the factorial of an integer.\n Recursive or loop variants are permitted."
    )
    factorial.new_test_case(True, "5", "120")
    factorial.new_test_case(True, "0", "1")
    factorial.new_test_case(False, "10", "3628800")

    manager.add_challenge(factorial)
    print(vars(manager.get_challenge_by_id(7)))
    print([vars(x) for x in manager.get_challenge_by_id(7).test_cases])
