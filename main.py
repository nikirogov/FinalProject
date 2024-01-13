import sqlite3
from Movies import Movies
from Users import Users

conn = sqlite3.connect('db.db')
cur = conn.cursor()
user_id = 0
def register():
    global user_id
    if user_id != 0:
        print("You are already logged in.")
        return
    nickname = input("Nickname: ")
    if Users().check_if_in_userlist(cur, nickname) == True:
        print("You are already registered, you can login with the command 'login' ")
        return
    first_name = input("First name: ")
    last_name = input("Last name: ")
    password = input("Password: ")

    Users().register(conn, cur, nickname, first_name, last_name, password)
    user_id = Users().get_user_id(cur, nickname)

def login():
    global user_id
    if user_id != 0:
        print("You are already logged in.")
        return
    nickname = input("Nickname: ")
    if not Users().check_if_in_userlist(cur, nickname):
        print("User not found. Try again. You can register with the command 'register' ")
        return
    password = input("Password: ")
    Users().login(cur, nickname, password)
    user_id = Users().get_user_id(cur, nickname)


def movlst():
    Movies().movlst(cur)

def movdt():
    given_movie = input("Insert movie you want details about: ")
    Movies().movdt(cur, given_movie)

def movsrch():
    type_of_search = input("Insert your search type (title, director or genre): ")
    if type_of_search == 'title':
        search_input = input("Insert title: ")
        Movies().movsrch_title(cur, search_input)
    if type_of_search == 'director':
        search_input = input("Insert director: ")
        Movies().movsrch_director(cur, search_input)
    if type_of_search == 'genre':
        search_input = input("Insert genre: ")
        Movies().movsrch_genre(cur, search_input)
def movlike():
    while True:
        user_input = input("Insert your new liked movie (if you want to see your liked movies list, type likelist)): ")
        if user_input == 'likelist':
            print("Your liked movies list:")
            Movies().movlike(cur, user_id)
            break
        movie_id = Movies().get_movie_id(cur, user_input)
        if not movie_id:
            print('No such movie found, enter new one')
            continue
        cur.execute("INSERT INTO user_likes (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
        cur.execute('''
        UPDATE movies
        SET like_count = (
            SELECT COUNT(*)
            FROM user_likes
            WHERE user_likes.movie_id = movies.id
        )
    ''')
        conn.commit()
def movfv():
    while True:
        user_input = input("Insert your new favorite movie (if you want to see your favorite movies list, type favlist)): ")
        if user_input == 'favlist':
            print("Your favorites list:")
            Movies().movfv(cur, user_id)
            break
        if user_input == 'end':
            break
        movie_id = Movies().get_movie_id(cur, user_input)
        if not movie_id:
            print('No such movie found, enter new one')
            continue
        cur.execute("INSERT INTO user_favorites (user_id, movie_id) VALUES (?, ?)", (user_id, movie_id))
        cur.execute('''
    UPDATE movies
    SET favorites_count = (
        SELECT COUNT(*)
        FROM user_favorites
        WHERE user_favorites.movie_id = movies.id
    )
''')
        conn.commit()
def movadd():
    global user_id
    title = input("Movie that you want to add to the database: ")
    if Movies().check_if_in_movlist(cur, title) == True:
        print("Movie already in the database")
    else:
        desc = input("Add a description to your movie: ")
        date = input("Add the movie's date of creation: ")
        director = input("Add the movie's director: ")
        genre = input("Add the movie's genre: ")

        Movies().movadd(conn,cur, title, desc, date, director, genre)
def movcat():
    type_of_cat = input("Insert your category (most_liked, genres, newest): ")

    if type_of_cat == 'most_liked':
        Movies().most_liked(cur)
    while type_of_cat == 'genres':
        given_genre = input("Top 5 in which genre? ")
        try:
            Movies().genres(cur, given_genre.lower())
            break
        except Exception as e:
            print(f"No movies having the genre: {given_genre}")
            retry = input("Do you want to try again? (yes/no): ")
            if retry.lower() != 'yes':
                break

    if type_of_cat == 'newest':
        Movies().newest(cur)



command = input("login or register: ")
while command != 'login' and command !='register':
    command = input("login or register: ")
    if command == 'login' or command == 'register':
        break
while command != 'end':
    if command == 'movlst':
        movlst()
    elif command == 'movdt':
        movdt()
    elif command == 'movcat':
        movcat()
    elif command == 'movsrch':
        movsrch()
    elif command == 'movadd':
        movadd()
    elif command == 'movfv':
        movfv()
    elif command == 'movlike':
        movlike()
    elif command == 'register':
        register()
    elif command == 'login':
        login()
    else:
        print("Invalid command")
    command = input("Your command: ")
print('Have a nice day!')
conn.close()