import base64
import os
import sqlite3
from flask import Flask, render_template, request
from card import Card

app = Flask(__name__)
import os


def get_portraits_from_folder(folder_path):
    portrait_data = []
    portrait_files = os.listdir(folder_path)

    for filename in portrait_files:
        # Split the filename into the name and extension parts (we don't need the extension)
        name, extension = os.path.splitext(filename)

        # Capitalize the name and add it to the portrait_data list
        portrait_data.append((name.capitalize(), name))

    return portrait_data

def get_sigils_from_folder(folder_path):
    # Connect to the database
    conn = sqlite3.connect('../database/inscryption.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, filename FROM sigils')
    db_sigils = cursor.fetchall()

    sigil_data = []
    sigil_files = os.listdir(folder_path)

    for filename in sigil_files:
        # Split the filename into the name and extension parts (we don't need the extension)
        name, extension = os.path.splitext(filename)

        # If sigils have an identified name in the database, rename it to that.
        for row in db_sigils:
            if name == row[1]:
                name = row[0]

        # Capitalize the name and add it to the portrait_data list
        sigil_data.append((name.capitalize(), name))

    return sigil_data

def get_database_data():
    # Connect to the database
    conn = sqlite3.connect('../database/inscryption.db')
    cursor = conn.cursor()
    database_data = {}

    # Query the database to retrieve decals
    cursor.execute('SELECT name, filename FROM decals')
    database_data['decals'] = cursor.fetchall()

    # Query the database to retrieve rarities
    cursor.execute('SELECT name, filename FROM rarities')
    database_data['rarities'] = cursor.fetchall()

    # Query the database to retrieve tribes
    cursor.execute('SELECT name, filename FROM tribes')
    database_data['tribes'] = cursor.fetchall()

    # Query the database to retrieve temples
    cursor.execute('SELECT name, filename FROM temples')
    database_data['temples'] = cursor.fetchall()

    # Query the database to retrieve staticons
    cursor.execute('SELECT name FROM staticons')
    database_data['staticons'] = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Get portraits from folder
    folder_path = '../resource/portraits'
    portrait_data = get_portraits_from_folder(folder_path)
    database_data['portraits'] = portrait_data

    # Get sigils from folder
    folder_path = '../resource/sigils'
    sigil_data = get_sigils_from_folder(folder_path)
    database_data['sigils'] = sigil_data

    return database_data

@app.route('/')
def index():
    db_data = get_database_data()
    return render_template('index.html', decals=db_data['decals'], tribes = db_data['tribes'],
                           temples = db_data['temples'], sigils = db_data['sigils'],
                           rarities = db_data['rarities'], portraits = db_data['portraits'],
                           staticons = db_data['staticons'], image_base64 = None)


@app.route('/generate_card', methods = ['POST'])
def generate_card_view():
    # Connect to the database
    conn = sqlite3.connect('../database/inscryption.db')
    cursor = conn.cursor()

    # Get user input from the form
    flags = []
    name = request.form.get('name')
    portrait = request.form.get('portrait')
    if portrait == 'None':
        flags.append('no_portrait')
    power = request.form.get('power')
    health = request.form.get('health')
    blood_cost = int(request.form.get('blood_cost')) if request.form.get('blood_cost') is not None else 0
    bone_cost = int(request.form.get('bone_cost')) if request.form.get('bone_cost') is not None else 0
    energy_cost = int(request.form.get('energy_cost')) if request.form.get('energy_cost') is not None else 0
    multi_cost_1 = request.form.get('multi_cost_1')
    multi_cost_2 = request.form.get('multi_cost_2')
    multi_cost_3 = request.form.get('multi_cost_3')
    multi_cost_4 = request.form.get('multi_cost_4')
    multi_cost = [multi_cost_1, multi_cost_2, multi_cost_3, multi_cost_4]
    multi_cost = [cost for cost in multi_cost if cost != 'None']
    print(multi_cost)
    rarity = request.form.get('rarity')
    temple = request.form.get('temple')
    decals = request.form.getlist('decals')
    before_decals = request.form.getlist('before_decals')
    tribes = request.form.getlist('tribes')
    first_sigil = request.form.getlist('first_sigil')
    first_sigil = {'sigil_filename': first_sigil[0], 'priority': 1}
    second_sigil = request.form.getlist('second_sigil')
    second_sigil = {'sigil_filename': second_sigil[0], 'priority': 2}
    staticon = request.form.getlist('staticon')
    card_type = request.form.get('card_type')
    golden = request.form.get('golden')
    emission = request.form.get('emission')
    if card_type == 'border':
        flags.append('card_border')
    elif card_type == 'bleed':
        flags.append('card_border')
        flags.append('card_bleed')
    if emission == 'True':
        flags.append('emission')
    if golden == 'True':
        flags.append('emission')
        flags.append('golden')

    cost = ''
    if blood_cost != 0:
        cost = 'blood_'+str(blood_cost)
    elif bone_cost != 0:
        cost = 'bone_'+str(bone_cost)
    elif energy_cost != 0:
        cost = 'energy_'+str(energy_cost)
    elif len(multi_cost) != 0:
        for next_cost in multi_cost:
            add = '[' + next_cost + ']'
            cost += add
            pass
    else:
        cost = None
    print(cost)
    card_data = {'name': f'{name}', 'filename': f'{portrait}',
                         'power': power, 'health': health, 'cost': f'{cost}', 'rarity': f'{rarity}', 'temple': f'{temple}',
                         'note_id': None}
    tribe_data = [{'tribe_filename': tribe} for tribe in tribes]
    if first_sigil['sigil_filename'] == 'None' and second_sigil['sigil_filename'] == 'None':
        sigil_data = []
    elif first_sigil['sigil_filename'] != 'None' and second_sigil['sigil_filename'] == 'None':
        sigil_data = [first_sigil,]
    elif first_sigil['sigil_filename'] == 'None' and second_sigil['sigil_filename'] != 'None':
        sigil_data = [second_sigil, ]
    else:
        sigil_data = [first_sigil, second_sigil]
    flag_data = [{'flag_filename': flag} for flag in flags]
    decal_data = [{'decal_filename': decal} for decal in decals]
    before_decal_data = [{'before_decal_filename': before_decal} for before_decal in before_decals]
    deathcard_data = None
    if staticon != ['None']:
        staticon_data = [{'staticon_filename': icon} for icon in staticon]
    else:
        staticon_data = []
    category_data = None
    # Generate the card based on user input
    image_base64 = Card(cursor, '../', card_data, tribe_data, sigil_data, flag_data,
                 before_decal_data, decal_data, deathcard_data, staticon_data, category_data).generate_card_image()
    image_base64 = base64.b64encode(image_base64).decode('utf-8')

    db_data = get_database_data()
    return render_template('index.html', decals = db_data['decals'], tribes = db_data['tribes'],
                           temples = db_data['temples'], sigils = db_data['sigils'],
                           rarities = db_data['rarities'], portraits = db_data['portraits'],
                           staticons = db_data['staticons'], before_decals = db_data['decals'],
                           image_base64 = image_base64)

if __name__ == '__main__':
    app.run(debug = True)
