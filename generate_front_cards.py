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
        card_image_buffer = card.generate_card_image()
        if card.filename is None:
            name = card.name
        else:
            name = card.filename
        with open(f'output/{name}.png', 'wb') as image_file:
            image_file.write(card_image_buffer)


if __name__ == '__main__':
    generate()
