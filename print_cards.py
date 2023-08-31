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
                if value == 'None':
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
            elif key == 'name':
                json_payload['name'] = value
                if value == 'Hungry Child':
                    json_payload['child'] = True
            elif key == 'power':
                if value.lower() == 'spilled blood':
                    json_payload['power'] = 0
                    json_payload['staticon'] = 'sacrificesthisturn'
                elif value.lower() in ('bell', 'cardsinhand', 'mirror', 'bones', 'ants'):
                    json_payload['power'] = 0
                    json_payload['staticon'] = value.lower()
                else:
                    json_payload['power'] = int(value)
            elif key == 'health':
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
            elif key == 'Blood2':
                json_payload['blood2'] = True
    return json_payload


def make_request(card_data):
    for card_info in card_data:
        endpoint_url = f'http://localhost:8080/api/card/leshy/front?locale=default'
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
            'terrain': False,
            'terrainLayout': False,
            'rare': False,
            'golden': False,
            'squid': False,
            'fused': False,
            'smoke': False,
            'child': False,
        }

        json_payload = process_card_info(card_info, json_payload)
        json_payload = {key: value for key, value in json_payload.items() if value is not None}
        print(json_payload)

        endpoint_url = 'http://localhost:8080/api/card/leshy/front?locale=default'''
        response = requests.post(endpoint_url, json = json_payload)

        if response.status_code == 201:
            image_data = response.content  # Get the binary image data
            file_name = os.path.join(output_folder, json_payload['name'] + '.png')
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

    card_data = read_entries('Leshy Cards.txt')
    make_request(card_data)

