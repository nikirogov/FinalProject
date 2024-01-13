import sqlite3
import Levenshtein as lev
from fuzzywuzzy import fuzz


class Movies:
    def __init__(self,title="",desc="",date="",director="",genre=""):
        self.title = title
        self.desc = desc
        self.date = date
        self.director = director
        self.genre = genre

    def add_movie(self, conn, cursor):
        cursor.execute('''
               INSERT INTO movies (title, description, release_date, director, genre)
               VALUES (?, ?, ?, ?, ?)
           ''', (self.title, self.desc, self.date, self.director, self.genre))
        conn.commit()

    def get_movie_id(self, cursor, title):
        cursor.execute('SELECT id FROM movies WHERE title = ?', (title,))
        result = cursor.fetchone()
        return result[0] if result else None
    def check_if_in_movlist(self, cursor, title):
        cursor.execute('SELECT * FROM movies WHERE title = ?', (title,))
        row = cursor.fetchone()

        if row:
            flag = True
        else:
            flag = False
        return flag
    def movlst(self, cursor):
        cursor.execute('SELECT * FROM movies')
        rows = cursor.fetchall()
        [print(row) for row in rows]

    def movdt(self, cursor, given_movie):
        cursor.execute('SELECT * FROM movies WHERE title = ?', (given_movie,))
        row = cursor.fetchone()
        if self.check_if_in_movlist(cursor, given_movie):
            print(row)
            return
        print(f"The movie {given_movie} is not found in the database")
        given_movie = input("Insert movie you want details about: ")

    def movsrch_title(self, cursor, search_input):
        cursor.execute('SELECT * FROM movies')
        rows = cursor.fetchall()
        search_results = []
        for row in rows:
            mistake_number = lev.distance(search_input,row[1])
            partial_match = fuzz.partial_ratio(search_input.lower(), row[1].lower())
            if mistake_number < 5 or partial_match > 80:
                search_results.append(row[1])
        print(search_results)

    def movsrch_director(self, cursor, search_input):
        cursor.execute('SELECT * FROM movies')
        rows = cursor.fetchall()
        search_results = []
        for row in rows:
            mistake_number = lev.distance(search_input,row[4])
            partial_match = fuzz.partial_ratio(search_input.lower(), row[4].lower())
            if mistake_number < 5 or partial_match > 80:
                search_results.append(row[1])
        print(search_results)

    def movsrch_genre(self, cursor, search_input):
        cursor.execute('SELECT * FROM movies')
        rows = cursor.fetchall()
        search_results = []
        for row in rows:
            mistake_number = lev.distance(search_input,row[5])
            partial_match = fuzz.partial_ratio(search_input.lower(), row[5].lower())
            if mistake_number < 3 or partial_match > 90:
                search_results.append(row[1])
        print(search_results)
    def movfv(self, cursor, user_id):
        cursor.execute('''
            SELECT *
            FROM movies
            JOIN user_favorites ON movies.id = user_favorites.movie_id
            WHERE user_favorites.user_id = ?;
        ''', (user_id,))
        rows = cursor.fetchall()
        for row in rows:

            print(row[1])
    def movlike(self, cursor, user_id):
        cursor.execute(f'''
            SELECT * FROM movies
            JOIN user_likes ON movies.id = user_likes.movie_id
            WHERE user_likes.user_id = {user_id};
            ''')
        rows = cursor.fetchall()
        for row in rows:

            print(row[1])
    def movadd(self, conn, cursor, title, desc, date, director, genre):
        cursor.execute('''
           INSERT INTO movies (title, description, release_date, director, genre)
           VALUES (?, ?, ?, ?, ?)
              ''', (title, desc, date, director, genre))
        print(f'The movie {title} has been added to the database')
        conn.commit()

    def genres(self, cursor, given_genre):
        given_genre_lower = given_genre.lower()  # Convert user input to lowercase
        cursor.execute('SELECT * FROM movies WHERE LOWER(genre) = ? ORDER BY like_count DESC LIMIT 5',
                       (given_genre_lower,))
        rows = cursor.fetchall()
        if not rows:
            raise Exception("No movies found for the given genre")
        for row in rows:
            print(row[1])

    def most_liked(self, cursor):
        cursor.execute('SELECT * FROM movies ORDER BY like_count DESC LIMIT 5')
        rows = cursor.fetchall()
        for row in rows:
                print(row[1])

    def newest(self, cursor):
        cursor.execute('SELECT * FROM movies ORDER BY release_date DESC LIMIT 5')
        rows = cursor.fetchall()
        for row in rows:

            print(row[1])