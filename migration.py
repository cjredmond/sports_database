import psycopg2
import csv

connection = psycopg2.connect("dbname=atletico_fifa user=atletico_fifa")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS player_data;")

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
cursor.execute(create_table_command)
with open('atletico_players.csv') as csvfile:
    read = csv.reader(csvfile, delimiter=',')
    for row in read:
        cursor.execute("INSERT INTO player_data VALUES(%s,%s,%s,%s,%s,%s)",(row[0],row[1],row[2],row[3],row[4],row[5]) )

connection.commit()
cursor.close()
connection.close()
