import psycopg2

class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn;
        self.cur = self.conn.cursor()
    def new_challenge_id(self):
        self.cur.execute("SELECT MAX(id) FROM Challenges")
        count=self.cur.fetchone()[0]
        return (count+1 if count not in [None, 0] else 0)
    def new_testcase_id(self):
        self.cur.execute("SELECT COUNT(id) FROM TestCases")
        count=self.cur.fetchone()[0]
        return (count+1 if count not in [None, 0] else 0)
    def add_challenge(self, chal):
        chal.id = self.new_challenge_id()
        self.cur.execute("INSERT INTO Challenges (id, title, author_id, description, instructions) VALUES (%s, '%s', %s, '%s', '%s');"
         % (chal.id, chal.title, chal.author_id, chal.desc, chal.instructions))
        for case in chal.test_cases:
            self.add_testcase(chal.id, case)
        conn.commit()
    def add_testcase(self, chal_id, test_case):
        test_case.id = self.new_testcase_id()
        self.cur.execute(f"INSERT INTO TestCases VALUES ({test_case.id}, {chal_id}, {test_case.shown}, '{test_case.specified_input}', '{test_case.specified_output}');")

    def delete_challenge(self, chal_id):
        self.cur.execute(f"DELETE FROM Challenges WHERE id={chal_id}")
        self.cur.execute(f"DELETE FROM TestCases WHERE challenge_id={chal_id}")
        conn.commit()
        pass
    def update_challenge(self, chal):
        pass
    def get_challenge_by_id(self, chal_id):
        pass
    def get_challenges_by_user(self, user_id):
        pass
    def get_challenges_by_kewords(self, search_term):
        pass

class Challenge:
    def __init__(self, chal_id, title, author_id, desc, instructions, test_cases=[]):
        self.id = chal_id
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

    print(manager.new_challenge_id())
    print(manager.new_testcase_id())

    manager.delete_challenge(0)
    manager.delete_challenge(1)
    print(manager.new_challenge_id())
    print(manager.new_testcase_id())