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
    print("""       Atletico Lineup:
              Torres   Greizmann
Carrasco    Saul        Gabi(c)       Koke
Felipe      Godin       Savic       Juanfran
                Oblak
""")


def search_two(field):
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

# numerical_search("rating", ">=")
# search_two("position")
# team()

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
    print("HERE")
    cursor.execute("INSERT INTO player_data VALUES(%s,%s,%s,%s,%s,%s)",(info[0],info[1],info[2],info[3],info[4],info[5]) )
    connection.commit()

add_player(new_player_data())
numerical_search("rating" ,">=")
cursor.close()
connection.close()
