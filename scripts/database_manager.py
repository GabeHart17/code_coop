import psycopg2

user_id = 0

class DatabaseManager:
    def __init__(self, conn_data):
        self.conn = psycopg2.connect(conn_data)
        self.cur = conn.cursor()
    def get_number_of_challenges(self):
        self.cur.execute("SELECT COUNT(id) FROM Challenges")
        return self.cur.fetchone()[0]

    def add_challenge(chal):
        chal.id = self.get_number_of_challenges()
        self.cur.execute(f"INSERT INTO Challenges VALUES ({chal.id}, {chal.title}, {chal.author_id}, {chal.desc}, {chal.instructions});")

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
    def new_test_case(shown, specified_input, specified_output):
        self.test_cases.append(-1, shown, specified_input, specified_output))

class TestCase:
    def __init__(self, case_id, shown, specified_input, specified_output):
        self.case_id = case_id
        self.shown = shown
        self.specified_input = specified_input
        self.specified_output = specified_output
