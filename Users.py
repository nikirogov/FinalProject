import hashlib
class Users:
    def __init__(self, nickname="", first_name="", last_name="", password=""):
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def create_table(self, conn, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                nickname TEXT,
                password_hash TEXT
            )
        ''')
        conn.commit()
    def get_user_id(self, cursor, nickname):
        cursor.execute('SELECT id FROM users WHERE nickname = ?', (nickname,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None
    def register(self, conn, cursor, nickname, first_name, last_name, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, nickname, password_hash)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, nickname, password_hash))
        conn.commit()
    def login(self, cursor, nickname, password):
        cursor.execute('SELECT * FROM users WHERE nickname = ?', (nickname,))
        user = cursor.fetchone()
        stored_hash_password = user[4]
        if self.check_password(password, stored_hash_password):
            print("Login successful!")
        else:
            print("Incorrect password. Try again.")
    def check_password(self, password, stored_hash_password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == stored_hash_password
    def check_if_in_userlist(self, cursor, nickname):
        cursor.execute('SELECT * FROM users WHERE nickname = ?', (nickname,))
        row = cursor.fetchone()
        return bool(row)

    def user_list(self, cursor):
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
