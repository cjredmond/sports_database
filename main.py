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

def show_all():
    sql = "SELECT * FROM player_data ORDER BY name ASC"
    cursor.execute(sql)
    results = cursor.fetchall()
    print_all_columns(results)

def print_all_columns(results):
    for row in results:
        print("""Player name: {}, Position: {}, Nationality: {}, Player rating: {}, Player age: {}.
""".format(row[1].title(),row[2].upper(),row[3].title(),row[4],row[5]))

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
    sql = "SELECT * FROM player_data ORDER BY %s %s limit %s;"
    cursor.execute(sql % (three_things[0],three_things[1],three_things[2]))
    results = cursor.fetchall()
    print_all_columns(results)

def search(field):
    choice = input("What is the {} you want to search for?".format(field)).lower()
    #sql = "SELECT * FROM player_data WHERE {} = %s;".format(field)
    sql = "SELECT * FROM player_data WHERE %s = '%s';"
    cursor.execute(sql % (field,choice))
    results = cursor.fetchall()
    print_all_columns(results)

def numerical_search(field,boolean):
    choice = input("What is the {} you want to search for?".format(field)).lower()
    sql = "SELECT * FROM player_data WHERE %s %s %s;"
    cursor.execute(sql % (field, boolean, choice))
    results = cursor.fetchall()
    print_all_columns(results)

count = 22
def new_player_data():
    new_name = input("What is the new player name?  >").lower()
    new_position = input("What is the new player position?\nChoose from: GK,CB,WB,CM,WF,ST  >").lower()
    new_country = input("What is the new player nationality?  >").lower()
    new_rating = input("What is the new player's rating (must be a # 0-99)?  >")
    if new_rating.isalpha() == True:
        print("Thats not a number")
        new_player_data()
    elif int(new_rating) not in range(99):
        print("Between 0-99")
        new_player_data()
    new_age = input("What is the new player's age (must be a # 0-99)?  >")
    while int(new_age) > 99:
        new_age = input("What is the new player's age (must be a # 0-99)?  >")

    global count
    new_id = count
    count = count +1
    return new_id,new_name,new_position,new_country,new_rating,new_age

def add_player(info):
    cursor.execute("INSERT INTO player_data VALUES(%s,%s,%s,%s,%s,%s)",(info[0],info[1],info[2],info[3],info[4],info[5]) )
    connection.commit()

def user_chooses_search():
    choice = input("Search by player (N)ame, (P)osition, (C)ountry, (R)ating, or (A)ge?\n>").upper()
    if choice == "N":
        search("name")
    elif choice == "P":
        print("The positions are: GK,CB,WB,CM,WF,ST")
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
    choice = input("Do you want to (A)dd a player, (S)earch, show a (T)op list, (U)pdate a player, or (D)isplay all players?\n>").upper()
    if choice in ["A", "S", "T", "U", "D"]:
        return choice
    else:
        print("Enter a valid answer")
        add_or_search_or_top()

def main_function():
    user_choice = add_or_search_or_top()
    if user_choice == "D":
        show_all()
        main_function()
    elif user_choice == "A":
        add_player(new_player_data())
        main_function()
    elif user_choice == "S":
        user_chooses_search()
        main_function()
    elif user_choice == "T":
        top_sort(user_chooses_sort())
        main_function()
    elif user_choice == "U":
        update(update_choice())
        main_function()
    else:
        main_function()

def update_choice():
    player = input("Who do you want to edit?\n>")
    field = input("What category do you want to edit? (P)osition, (R)ating, (A)ge, (N)ationality.\n>").upper()
    if field == "P":
        return_field = "position"
    elif field == "R":
        return_field = "rating"
    elif field == "A":
        return_field = "Age"
    elif field == "N":
        return_field = "country"
    return player,return_field

def update(info):
    sql = "UPDATE player_data SET %s = '%s' WHERE name = '%s';"
    stat = input("What is the new value for {} {}?\n:".format(info[0].title(),info[1].title()))
    cursor.execute(sql , (info[1],stat,info[0]))
    connection.commit()

def program_running():
    print("Welcome to the Atletico Madrid player database")
    print("The player's name, position, nationality, FIFA rating, and age can be searched")
    team()
    main_function()


program_running()

cursor.close()
connection.close()
