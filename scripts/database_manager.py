import psycopg2

class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn;
        self.cur = self.conn.cursor()
    def get_challenge_count(self):
        self.cur.execute("SELECT COUNT(id) FROM Challenges")
        return self.cur.fetchone()[0]
    def get_testcase_count(self):
        self.cur.execute("SELECT COUNT(id) FROM TestCases")
        return self.cur.fetchone()[0]
    def add_challenge(self, chal):
        chal.id = self.get_challenge_count()
        self.cur.execute("INSERT INTO Challenges (id, title, author_id, description, instructions) VALUES (%s, '%s', %s, '%s', '%s');"
         % (chal.id, chal.title, chal.author_id, chal.desc, chal.instructions))
        current_casecount = self.get_testcase_count()
        for case in chal.test_cases:
            self.add_testcase(chal.id, case)
        conn.commit()
    def add_testcase(self, chal_id, test_case):
        test_case.id = self.get_testcase_count()
        self.cur.execute(f"INSERT INTO TestCases VALUES ({test_case.id}, {chal_id}, {test_case.shown}, '{test_case.specified_input}', '{test_case.specified_output}');")

    def delete_challenge(chal):
        pass
    def update_challenge(chal):
        pass
    def get_challenge_by_id(chal_id):
        pass
    def get_challenges_by_user(user_id):
        pass
    def get_challenges_by_kewords(search_term):
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
    
    manager.add_challenge(factorial)