import psycopg2
import csv
create_table_command = """
CREATE TABLE player_data (
    id serial PRIMARY KEY,
    name VARCHAR(20),
    position VARCHAR(20),
    country VARCHAR(20),
    rating NUMERIC(2),
    age NUMERIC(2)
);

"""
connection = psycopg2.connect("dbname=atletico_fifa")
cursor = connection.cursor()

def team():
    print("""           Atletico Lineup: \n
              Torres   Greizmann
Carrasco    Saul        Gabi(c)       Koke
Felipe      Godin       Savic       Juanfran
                Oblak
""")

def user_chooses_sort():
    print("You can search player rating and age from the top or bottom")
    field = input("(R)ating or (A)ge?  : ").upper()
    up_down = input("(T)op or (B)ottom?  : ").upper()
    amount = input("How many should show? (#)  ").upper()
    return_field = ""
    return_up_down = ""
    if field == "R":
        return_field = "rating"
    elif field == "A":
        return_field = "age"
    else:
        pass
    if up_down == "T":
        return_up_down = "DESC"
    else:
        pass
    return return_field,return_up_down,amount

def top_sort(three_things):
    sql = "SELECT * FROM player_data ORDER BY {} {} limit {};".format(three_things[0],three_things[1],three_things[2])
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print("""Player name: {}, Position: {}, Nationality: {}, Player rating: {}, Player age: {}.
""".format(row[1].title(),row[2].upper(),row[3].title(),row[4],row[5]))




def search(field):
    choice = input("What is the {} you want to search for?".format(field)).lower()
    sql = "SELECT * FROM player_data WHERE {} = %s;".format(field)
    cursor.execute(sql,(choice,))
    results = cursor.fetchall()
    for row in results:
        print("""Player name: {}, Position: {}, Nationality: {}, Player rating: {}, Player age: {}.
""".format(row[1].title(),row[2].upper(),row[3].title(),row[4],row[5]))


def numerical_search(field,boolean):
    choice = input("What is the {} you want to search for?".format(field)).lower()
    sql = "SELECT * FROM player_data WHERE {} {} %s;".format(field,boolean)
    cursor.execute(sql,(choice,))
    results = cursor.fetchall()
    for row in results:
        print("""Player name: {}, Position: {}, Nationality: {}, Player rating: {}, Player age: {}.
""".format(row[1].title(),row[2].upper(),row[3].title(),row[4],row[5]))

count = 22
def new_player_data():
    new_name = input("What is the new player name?  >")
    new_position = input("What is the new player position?  >")
    new_country = input("What is the new player nationality?  >")
    new_rating = input("What is the new player's rating?  >")
    new_age = input("What is the new player's age?  >")
    global count
    new_id = count
    count = count +1

    return new_id,new_name,new_position,new_country,new_rating,new_age

def add_player(info):
    cursor.execute("INSERT INTO player_data VALUES(%s,%s,%s,%s,%s,%s)",(info[0],info[1],info[2],info[3],info[4],info[5]) )
    connection.commit()

def user_chooses_search():
    choice = input("Search by player (N)ame, (P)osition, (C)ountry, (R)ating, or (A)ge?  >").upper()
    if choice == "N":
        search("name")
    elif choice == "P":
        search("position")
    elif choice == "C":
        search("country")
    elif choice == "R":
        print("You will search for player ratings (comparison) (number)")
        search_parameter = input("Enter a (=), (>), (>=), (<=), or (<)  :")
        numerical_search("rating", str(search_parameter))
    elif choice == "A":
        print("You will search for player ages (comparison) (number)")
        search_parameter = input("Enter a (=), (>), (>=), (<=), or (<)  :")
        numerical_search("age", str(search_parameter))
    else:
        print("Please enter valid character")
        user_chooses_search()

def add_or_search_or_top():
    choice = input("Do you want to (A)dd a player, (S)earch, or show a (T)op list?").upper()
    if choice == "A":
        return "A"
    elif choice == "S":
        return "S"
    elif choice == "T":
        return "T"
    else:
        print("Enter a valid answer")
        add_or_search_or_top()

def main_function():
    user_choice = add_or_search_or_top()
    if user_choice == "A":
        add_player(new_player_data())
        main_function()
    elif user_choice == "S":
        user_chooses_search()
        main_function()
    elif user_choice == "T":
        top_sort(user_chooses_sort())
        main_function()
    else:
        main_function()


def program_running():
    print("Welcome to the Atletico Madrid player database")
    print("The player's name, position, nationality, FIFA rating, and age can be searched")
    team()
    main_function()

def update():
    sql = "UPDATE atletico_players SET rating 99 WHERE name = 'saul';"
    cursor.execute(sql)
    results = cursor.fetchall()


program_running()


cursor.close()
connection.close()
