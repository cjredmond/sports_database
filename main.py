import psycopg2
connection = psycopg2.connect("dbname=atletico_fifa")
cursor = connection.cursor()
#name = input("What is the player you want to search for?").lower()
#country = input("country?").lower()
#cursor.execute("SELECT * FROM player_data WHERE name = %s;",(name,))
#results = cursor.fetchall()
#print(*results)
def team():
    print("""       Atletico Lineup:
              Torres   Geizmann
Carrasco    Saul        Gabi        Koke
Felipe      Godin       Savic       Juanfran
                Oblak
""")

def search():
    name = input("What is the player you want to search for?").lower()
    cursor.execute("SELECT * FROM player_data WHERE name = %s;",(name,))
    results = cursor.fetchall()
    for row in results:
        print("""Player name: {}, Position: {}, Nationality: {}, Player rating: {}, Player age: {}.
""".format(row[1].title(),row[2].upper(),row[3].title(),row[4],row[5]))
def search_two(field, string):
    data = input("What is the {} you want to search for?".format(string)).lower()
    sql = "SELECT * FROM player_data WHERE {} = %s;".format(field)
    print(sql)
    #cursor.execute("SELECT * FROM player_data WHERE %s = %s;",(field, data))
    cursor.execute(sql,(data,))
    results = cursor.fetchall()
    for row in results:
        print("""Player name: {}, Position: {}, Nationality: {}, Player rating: {}, Player age: {}.
""".format(row[1].title(),row[2].upper(),row[3].title(),row[4],row[5]))
search_two("position", "Position")
team()
search()


cursor.close()
connection.close()
