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
            card = Card(cursor, './', *row)
            if i == 1:
                card.flags.append('card_border')
                card_type = 'border'
            elif i == 2:
                card.flags.append('card_border')
                card.flags.append('card_bleed')
                card_type = 'print bleed'
            else:
                card_type = 'regular'

            # Get the card category from the database
            cursor.execute('SELECT category FROM card_categories WHERE card_filename = ?', (card.filename,))
            category = cursor.fetchone()[0]

            # Create the full directory path
            directory_path = os.path.join('output', 'cards', category, card.types['temple'], card_type)

            # Check if the directory exists, and create it if it doesn't
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # Generating the card image
            card_image_buffer = card.generate_card_image()
            #card.disconnect()

            with open(os.path.join(directory_path, f'{card.filename}.png'), 'wb') as image_file:
                image_file.write(card_image_buffer)

@db_connect
def generate_patches(cursor):
    # SELECT and fetch to retrieve all cards from table
    cursor.execute('SELECT * FROM sigils')
    rows = cursor.fetchall()

    for row in rows:
        patch = Patch('./', row[1], 'patch')

        # Create the full directory path for the sigil image
        source_file_path = f'resource/sigils/{patch.filename}.png'

        # Create the directory path for outputting sigils
        directory_path = os.path.join('output', 'sigils')

        # Check if the sigil image exists before attempting to generate a patch
        if not os.path.exists(source_file_path):
            continue  # Skip if it doesn't exist - likely an Act 2 sigil with no Act 1 equivalent

        # Check if the output directory exists, and create it if it doesn't
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        patch_image_buffer = patch.generate_patch_image()
        with open(os.path.join(directory_path, f'{patch.filename}.png'), 'wb') as image_file:
            image_file.write(patch_image_buffer)

if __name__ == '__main__':
    generate_front_cards()
    generate_patches()
