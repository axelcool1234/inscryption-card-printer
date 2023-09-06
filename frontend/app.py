import base64
import os
import sqlite3
from flask import Flask, render_template, request
from card import Card

app = Flask(__name__)
def get_portraits_from_folder(folder_path):
    portrait_data = []
    portrait_files = os.listdir(folder_path)

    for filename in portrait_files:
        capitalized_name = filename.capitalize()
        portrait_data.append((capitalized_name.strip('.png'), filename.strip('.png')))

    return portrait_data
def get_database_data():
    # Connect to the database
    conn = sqlite3.connect('../database/inscryption.db')
    cursor = conn.cursor()
    database_data = {}

    # Query the database to retrieve decals
    cursor.execute('SELECT name, filename FROM decals')
    database_data['decals'] = cursor.fetchall()
    print(database_data['decals'])

    # Query the database to retrieve rarities
    cursor.execute('SELECT name, filename FROM rarities')
    database_data['rarities'] = cursor.fetchall()

    # Query the database to retrieve tribes
    cursor.execute('SELECT name, filename FROM tribes')
    database_data['tribes'] = cursor.fetchall()

    # Query the database to retrieve temples
    cursor.execute('SELECT name, filename FROM temples')
    database_data['temples'] = cursor.fetchall()

    # Query the database to retrieve sigils
    cursor.execute('SELECT name, filename FROM sigils')
    database_data['sigils'] = cursor.fetchall()

    # Query the database to retrieve staticons
    cursor.execute('SELECT name FROM staticons')
    database_data['staticons'] = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Get portraits from folder
    folder_path = '../resource/portraits'
    portrait_data = get_portraits_from_folder(folder_path)
    database_data['portraits'] = portrait_data

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
    blood_cost = int(request.form.get('blood_cost'))
    bone_cost = int(request.form.get('bone_cost'))
    energy_cost = int(request.form.get('energy_cost'))
    orange_mox_cost = int(request.form.get('orange_mox_cost'))
    green_mox_cost = int(request.form.get('green_mox_cost'))
    blue_mox_cost = int(request.form.get('blue_mox_cost'))
    rarity = request.form.get('rarity')
    temple = request.form.get('temple')
    decals = request.form.getlist('decals')
    tribes = request.form.getlist('tribes')
    sigils = request.form.getlist('sigils')
    staticons = request.form.getlist('staticons')
    card_type = request.form.get('card_type')
    print(card_type)
    if card_type == 'border':
        flags.append('card_border')
    elif card_type == 'bleed':
        flags.append('card_border')
        flags.append('card_bleed')

    card_data = {'name': f'{name}', 'filename': f'{portrait}',
                         'power': power, 'health': health, 'blood_cost': blood_cost,
                         'bone_cost': bone_cost, 'energy_cost': energy_cost,
                         'orange_mox_cost': orange_mox_cost, 'green_most_cost': green_mox_cost,
                         'blue_mox_cost': blue_mox_cost, 'rarity': f'{rarity}', 'temple': f'{temple}',
                         'note_id': None}
    tribe_data = [{'tribe_filename': tribe} for tribe in tribes]
    sigil_data = [{'sigil_filename': sigil} for sigil in sigils]
    flag_data = [{'flag_filename': flag} for flag in flags]
    decal_data = [{'decal_filename': decal} for decal in decals]
    deathcard_data = None
    staticon_data = [{'staticon_filename': staticon} for staticon in staticons]
    category_data = None

    # Generate the card based on user input
    image_base64 = Card(cursor, '../', card_data, tribe_data, sigil_data, flag_data,
                 decal_data, deathcard_data, staticon_data, category_data).generate_card_image()
    image_base64 = base64.b64encode(image_base64).decode('utf-8')

    db_data = get_database_data()
    return render_template('index.html', decals = db_data['decals'], tribes = db_data['tribes'],
                           temples = db_data['temples'], sigils = db_data['sigils'],
                           rarities = db_data['rarities'], portraits = db_data['portraits'],
                           staticons = db_data['staticons'], image_base64 = image_base64)

if __name__ == '__main__':
    app.run(debug = True)
