import os
from card import Card
from patch import Patch
from helpers import db_connect

@db_connect
def generate_front_cards(cursor):
    # SELECT and fetch to retrieve all cards from table
    cursor.execute('SELECT * FROM cards')
    rows = cursor.fetchall()

    for i in range(3):
        # Generating all cards
        for row in rows:
            card = Card(*row)
            if i == 1:
                card.flags.append('card_border')
                directory = 'border'
            elif i == 2:
                card.flags.append('card_border')
                card.flags.append('card_bleed')
                directory = 'print bleed'
            else:
                directory = 'regular'
            card_image_buffer = card.generate_card_image()
            card.disconnect()
            with open(f'output/cards/{directory}/{card.filename}.png', 'wb') as image_file:
                image_file.write(card_image_buffer)

@db_connect
def generate_patches(cursor):
    # SELECT and fetch to retrieve all cards from table
    cursor.execute('SELECT * FROM sigils')
    rows = cursor.fetchall()

    for row in rows:
        patch = Patch(row[1], 'patch')

        source_file_path = f'resource/sigils/{patch.filename}.png'
        output_file_path = f'output/patches/{patch.filename}.png'

        # Check if the sigil image exists before attempting to generate a patch
        if not os.path.exists(source_file_path):
            continue  # Skip if it doesn't exist - likely an Act 2 sigil with no Act 1 equivalent

        patch_image_buffer = patch.generate_patch_image()
        with open(output_file_path, 'wb') as image_file:
            image_file.write(patch_image_buffer)

if __name__ == '__main__':
    #generate_front_cards()
    generate_patches()
