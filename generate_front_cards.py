from card import Card
from helpers import db_connect

@db_connect
def generate(cursor):
    # SELECT and fetch to retrieve all cards from table
    cursor.execute('SELECT * FROM cards')
    rows = cursor.fetchall()

    # Generating all cards
    for row in rows:
        card = Card(*row)
        print(card.name)

if __name__ == '__main__':
    generate()
