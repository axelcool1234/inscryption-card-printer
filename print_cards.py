import os
import requests

TRIBES_MAPPING = {
    'Feathered': 'bird',
    'Avian': 'bird',
    'Wolf': 'canine',
    'Canine': 'canine',
    'Hooved': 'hooved',
    'Reptilian': 'reptile',
    'Reptile': 'reptile',
    'Insect': 'insect',
    'Insectoid': 'insect'
}
SIGILS_MAPPING = {
    'Made of Stone': 'madeofstone',
    'Rabbit Hole': 'drawrabbits',
    'Bees Within': 'beesonhit',
    'Sprinter': 'strafe',
    'Touch of Death': 'deathtouch',
    'Fledgling': 'evolve',
    'Fledgling (1)': 'evolve_1',
    'Fledgling (2)': 'evolve_2',
    'Fledgling (3)': 'evolve_3',
    'Dam Builder': 'createdams',
    'Hoarder': 'tutor',
    'Burrower': 'whackamole',
    'Fecundity': 'drawcopy',
    'Loose Tail': 'tailonhit',
    'Corpse Eater': 'corpseeater',
    'Bone King': 'quadruplebones',
    'Waterborne': 'submerge',
    'Unkillable': 'drawcopyondeath',
    'Sharp Quills': 'sharp',
    'Hefty': 'strafepush',
    'Rampager': 'strafeswap',
    'Brood Parasite': 'createegg',
    'Armored': 'deathshield',
    'Double Strike': 'doublestrike',
    'Morsel': 'morsel',
    'Blood Lust': 'gainattackonkill',
    'Scavenger': 'opponentbones',
    'Finical Hatchling': 'hydraegg',
    'Ant Spawner': 'drawant',
    'Guardian': 'guarddog',
    'Airborne': 'flying',
    'Many Lives': 'sacrificial',
    'Repulsive': 'preventattack',
    'Worthy Sacrifice': 'tripleblood',
    'Mighty Leap': 'reach',
    'Bifurcated Strike': 'splitstrike',
    'Trifurcated Strike': 'tristrike',
    'Frozen Away': 'icecube',
    'Sinkhole': 'sinkhole',
    'Bone Digger': 'bonedigger',
    'Trinket Bearer': 'randomconsumable',
    'Steel Trap': 'steeltrap',
    'Amorphous': 'randomability',
    'Tidal Lock': 'squirrelorbit',
    'Moon Strike': 'allstrike',
    'Leader': 'buffneighbours',
    'Brittle': 'brittle',
    'Skeleton Crew': 'skeletonstrafe',
    'Green Mox': 'gaingemgreen',
    'Orange Mox': 'gaingemorange',
    'Blue Mox': 'gaingemblue',
    'Gem Animator': 'buffgems',
    'Ruby Heart': 'droprubyondeath',
    'Mental Gemnastics': 'gemsdraw',
    'Gem Dependant': 'gemdependant',
    'Great Mox': 'gaingemtriple',
    'Handy': 'drawnewhand',
    'Squirrel Shedder': 'squirrelstrafe',
    'Attack Conduit': 'conduitbuffattack',
    'Spawn Conduit': 'conduitfactory',
    'Healing Conduit': 'conduitheal',
    'Null Conduit': 'conduitnull',
    'Battery Bearer': 'gainbattery',
    'Detonator': 'explodeondeath',
    'Sniper': 'sniper',
    'Nano Armor': 'deathshield',
    'Overclocked': 'permadeath',
    'Bomb Latch': 'latchexplodeondeath',
    'Brittle Latch': 'latchbrittle',
    'Shield Latch': 'latchdeathshield',
    'Dead Byte': 'filesizedamage',
    'Hostage File': 'deletefile',
    'Transformer': 'transformer',
    'Sentry': 'sentry',
    'Gem Detonator': 'explodegems',
    'Gem Guardian': 'shieldgems',
    'Vessel Printer': 'drawvesselonhit',
    'Energy Conduit': 'conduitenergy',
    'Bomb Spewer': 'bombspawner',
    'Double Death': 'doubledeath',
    'Power Dice': 'activatedrandompowerenergy',
    'Enlarge': 'activatedstatsup',
    'Swapper': 'swapstats',
    'Disentomb': 'activateddrawskeleton',
    'Energy Gun': 'activateddealdamage',
    'Bellist': 'createbells',
    'Annoying': 'buffenemy',
    'Gem Spawn Conduit': 'conduitspawngems',
    'Gift Bearer': 'drawrandomcardondeath',
    'Looter': 'loot',
    'True Scholar': 'activatedsacrificedrawcards',
    'Stimulate': 'activatedstatsupenergy',
    'Marrow Sucker': 'activatedheal',
    'Stinky': 'debuffenemy',
    'Buff When Powered': 'cellbuffself',
    'Gift When Powered': 'celldrawrandomcardondeath',
    'Trifurcated When Powered': 'celltristrike',
    'Bonehorn': 'activatedenergytobones',
    'Clinger': 'movebeside',
    'WaterborneSquid': 'submergesquid',
    'Blood Guzzler': 'bloodguzzler',
    'Haunter': 'haunter',
    'Exploding Corpse': 'explodingcorpse',
    'Apparition': 'bloodymary',
    'Virtual Realist': 'virtualreality',
    'Head of Edaxio': 'edaxiohead',
    'Arms of Edaxio': 'edaxioarms',
    'Legs of Edaxio': 'edaxiolegs',
    'Torso of Edaxio': 'edaxiotorso'
}

def process_card_info(card_info, json_payload):
    for attribute in card_info:
        if attribute:
            key, value = attribute.split(': ', 1)
            key = key.lower()
            if key == 'tribes' or key == 'tribe':
                if value == 'None':
                    pass
                else:
                    tribes = [tribe.strip() for tribe in value.split(',')]
                    tribes = [TRIBES_MAPPING[tribe] for tribe in tribes]
                    json_payload['tribes'] = tribes
            elif 'orange' in value or 'green' in value or 'blue' in value:
                for gem in value.split(', '):
                    json_payload['gemCost'][gem] = True
            elif key == 'cost':
                if value.lower() == 'none':
                    pass
                elif value.split()[1].lower() == 'blood':
                    json_payload['bloodCost'] = int(value.split()[0])
                elif value.split()[1].lower() == 'bone' or value.split()[1].lower() == 'bones':
                    json_payload['boneCost'] = int(value.split()[0])
                elif value.split()[1].lower() == 'energy':
                    json_payload['energyCost'] = int(value.split()[0])
            elif key == 'sigils' or key == 'sigil':
                if value == 'None':
                    pass
                else:
                    sigils = [sigil.strip() for sigil in value.split(',')]
                    sigils = [SIGILS_MAPPING[sigil] for sigil in sigils]
                    json_payload['sigils'] = sigils
            elif key == 'temple':
                json_payload['temple'] = value.lower()
            elif key == 'portrait':
                if value == 'None':
                    capitalized_name = ' '.join(word.capitalize() for word in json_payload['name'].split())
                    json_payload['portrait'] = {'type': 'creature', 'creature': capitalized_name.replace(' ', '')}
                else:
                    json_payload['portrait'] = {'type':'creature','creature':value}
            elif key == 'deathcard':
                data = value.split(', ')
                json_payload['portrait'] = {'type':'deathcard','data':
                    {"head":data[0],"eyes":int(data[1][-1]) - 1, "mouth":int(data[2][-1]) - 1,"lostEye": True if data[3] == "True" else False}}
            elif key == 'name':
                json_payload['name'] = value
            elif key == 'power':
                if value.lower() == 'spilled blood':
                    json_payload['power'] = 0
                    json_payload['staticon'] = 'sacrificesthisturn'
                elif value.lower() in ('bell', 'cardsinhand', 'mirror', 'bones', 'ants'):
                    json_payload['power'] = 0
                    json_payload['staticon'] = value.lower()
                elif value.lower() == 'delete':
                    del json_payload['power']
                    json_payload['hidePowerAndHealth'] = True
                else:
                    json_payload['power'] = int(value)
            elif key == 'health':
                if value.lower() == 'delete':
                    del json_payload['health']
                    json_payload['hidePowerAndHealth'] = True
                else:
                    json_payload['health'] = int(value)
            elif key == 'type':
                if value.lower() == 'rare':
                    json_payload['rare'] = True
                elif value.lower() == 'terrain':
                    json_payload['terrain'] = True
                    json_payload['terrainLayout'] = True
                elif value.lower() == 'special terrain':
                    json_payload['terrain'] = True
                    json_payload['terrainLayout'] = False
            elif key == 'golden':
                json_payload['golden'] = True
            elif key == 'smoke':
                json_payload['smoke'] = True
            elif key == 'snelk':
                json_payload['snelk'] = True
            elif key == 'blood2':
                json_payload['blood2'] = True
            elif key == 'squid':
                json_payload['squid'] = True
            elif key == 'child':
                json_payload['child'] = True
            elif key == 'enhanced':
                json_payload['enhanced'] = True
            elif key == 'snelk4':
                json_payload['snelk4'] = True
    return json_payload


def make_request(card_data, endpoint_url):
    for card_info in card_data:
        json_payload = {
            'name': '',
            'power': 0,
            'staticon': None,
            'health': 1,
            'tribes': [],
            'bloodCost': 0,
            'boneCost': 0,
            'energyCost': 0,
            'gemCost':{'orange1':False,'green1':False,'blue1':False,
                       'orange2':False,'green2':False,'blue2':False,
                       'orange3':False,'green3':False,'blue3':False},
            'decals': [],
            'sigils': [],
            'temple': 'nature',
        }

        if endpoint_url != 'http://localhost:8080/api/card/leshy/front?locale=default':
            del json_payload['gemCost']
        json_payload = process_card_info(card_info, json_payload)
        json_payload = {key: value for key, value in json_payload.items() if value is not None}
        print(json_payload)

        response = requests.post(endpoint_url, json = json_payload)

        if response.status_code == 201:
            image_data = response.content  # Get the binary image data
            base_name = json_payload['name']
            file_name = os.path.join(output_folder, base_name + '.png')

            # Check if the file already exists
            counter = 1
            while os.path.exists(file_name):
                file_name = os.path.join(output_folder, f"{base_name}({counter}).png")
                counter += 1

            with open(file_name, 'wb') as image_file:
                image_file.write(image_data)
            print(f'Image downloaded successfully: {file_name}')
        else:
            print(f'Image download failed: {response.text}')
            break


def read_entries(file_path):
    entries = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    entry = []
    for line in lines:
        if line.strip().startswith('#'):
            continue
        if not line.strip():
            if entry:
                entries.append(entry)
                entry = []
        else:
            entry.append(line.strip())
    if entry:
        entries.append(entry)
    return entries


if __name__ == '__main__':
    output_folder = 'Output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    endpoint_url = f'http://localhost:8080/api/card/leshy/front?locale=default'
    card_data = read_entries('card_data/leshy.txt')
    make_request(card_data, endpoint_url)

    endpoint_url = f'https://api2.generator.cards/api/card/leshy/front?locale=default'
    card_data = read_entries('card_data/leshy.txt')
    make_request(card_data, endpoint_url)

    # TODO: Fix gold emissions
    # TODO: Add red emissions
