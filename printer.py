import os
import shutil
import sqlite3
import subprocess

from card import Card
from helpers import db_connect
from patch import Patch

def call_database(dict_mode, query, data=None):
    try:
        conn = sqlite3.connect('database/inscryption.db')
        if dict_mode is True:
            conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)

        result = cursor.fetchall()

        return result
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()
def get_data(table_name, filename):
    query = f'SELECT * FROM {table_name} WHERE card_filename = ?'
    rows = call_database(True, query, (filename,))
    data_as_dicts = [dict(row) for row in rows]
    return data_as_dicts
def generate_front_cards():
    cards = call_database(True, 'SELECT * FROM cards')

    for i in range(3):
        # Generating all cards
        for data in cards:
            card_data = dict(data)
            filename = card_data["filename"]
            tribe_data = get_data('card_tribes', filename)
            sigil_data = get_data('card_sigils', filename)
            flag_data = get_data('card_flags', filename)
            decal_data = get_data('card_decals', filename)
            before_decal_data = get_data('card_before_decals', filename)
            deathcard_data = get_data('death_cards', filename)
            deathcard_data = deathcard_data[0] if len(deathcard_data) == 1 else None
            staticon_data = get_data('card_staticons', filename)
            category_data = get_data('card_categories', filename)[0]['category']

            # Connect for card
            conn = sqlite3.connect('database/inscryption.db')
            cursor = conn.cursor()
            card = Card(cursor, './', card_data, tribe_data, sigil_data, flag_data,
                        before_decal_data, decal_data, deathcard_data, staticon_data, category_data)
            cursor.close()
            conn.close()
            if i == 1:
                card.flags.append('card_border')
                card_type = 'border'
            elif i == 2:
                card.flags.append('card_border')
                card.flags.append('card_bleed')
                card_type = 'print bleed'
            else:
                card_type = 'regular'

            # Create the full directory path
            directory_path = os.path.join('output', 'cards', card.category, card.temple, card_type)

            # Check if the directory exists, and create it if it doesn't
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # Generating the card image
            card_image_buffer = card.generate_card_image()

            with open(os.path.join(directory_path, f'{card.filename}.png'), 'wb') as image_file:
                image_file.write(card_image_buffer)

def generate_patches():
    conn = sqlite3.connect('database/inscryption.db')
    cursor = conn.cursor()

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

def open_templates():
    templates = {}
    for file in os.listdir("resource/latex_templates/"):
        with open(f"resource/latex_templates/{file}", "r") as template_file:
            templates[file.split(' ')[0].lower()] = template_file.read()
    return templates

def generate_latex(entries, font):
    #Get templates
    templates = open_templates()
    #Start with preamble (beginning of document)
    latex_content = templates["preamble"].replace("FONT", font)
    #Go through each entry and properly format it based off which type of entry it is.
    current_type = "None"
    for entry in entries:
        name, image_path, description = entry

        if current_type != image_path.split('/')[1]:
            current_type = image_path.split('/')[1]

            if current_type == "VariableStats":
                title = "Variable Stats"
            else:
                title = current_type
            latex_content += "\\newpage\n"
            latex_content += "\chaptertitle{" + f"{title}" + "}{0.5}\n"
            latex_content += "\\newpage\n"

            match current_type:
                case "Boons":
                    latex_content += "\customHeaderFooter{0.5}{1.75}{0.5}{1.75}\n"
                case "Items":
                    latex_content += "\customHeaderFooter{0.5}{1.75}{0.5}{1.75}\n"
                case "Sigils":
                    latex_content += "\customHeaderFooter{0.5}{1.75}{0.5}{1.75}\n"
                case "VariableStats":
                    latex_content += "\customHeaderFooter{0.5}{1.75}{0.5}{1.75}\n"
                case "Spells":
                    #I have no spells yet, don't need to worry about this case.
                    pass
        entry = templates[current_type].replace("NAME", name.strip('_'))
        entry = entry.replace("IMAGE_PATH", image_path)
        entry = entry.replace("DESCRIPTION", description) if description is not None else entry.replace("DESCRIPTION", 'None')
        entry = entry.replace("FONT", font)
        latex_content += entry
    #End of document
    latex_content += "\\end{document}"

    #Create tex file
    with open("output/rulebook.tex", "w") as tex_file:
        tex_file.write(latex_content)

def compile_latex_to_pdf():
    subprocess.run(["lualatex", "output/rulebook.tex"])
    # Run again to make sure references and TOC are generated properly
    subprocess.run(["lualatex", "output/rulebook.tex"])

    # Move generated files to the output folder
    generated_files = ["rulebook.pdf", "rulebook.aux", "rulebook.log"]
    for file in generated_files:
        shutil.move(file, f"output/rulebook/{file}")

@db_connect
def generate_rulebook(cursor):
    font = "HEAVYWEIGHT"
    entries = []
    # TODO: Eventually include spells if those are ever implemented
    # TODO: Add boons and items tables to database
    entry_types = ["boons", "items", "sigils", "staticons"]

    for entry_type in entry_types:
        cursor.execute(f'SELECT * FROM {entry_type}')
        rows = cursor.fetchall()
        for row in rows:
            row = dict(row)
            name = row['name']
            image_path = f'resource/{entry_type}/{row["filename"]}.png'
            description = cursor.execute(f'SELECT description FROM notes WHERE filename = ? AND type = ?', (row['filename'], entry_type)).fetchone()
            description = dict(description)['description'] if description is not None else None
            entries.append((name, image_path, description))

    generate_latex(entries, font)
    compile_latex_to_pdf()

if __name__ == '__main__':
    generate_front_cards()
    generate_patches()
    generate_rulebook()
