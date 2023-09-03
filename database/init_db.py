import sqlite3

# Connecting
conn = sqlite3.connect('inscryption.db')
cursor = conn.cursor()

# Dropping TABLEs
cursor.execute('DROP TABLE IF EXISTS flags;')
cursor.execute('DROP TABLE IF EXISTS staticons;')
cursor.execute('DROP TABLE IF EXISTS decals;')
cursor.execute('DROP TABLE IF EXISTS notes;')
cursor.execute('DROP TABLE IF EXISTS sigils;')
cursor.execute('DROP TABLE IF EXISTS tribes;')
cursor.execute('DROP TABLE IF EXISTS cards;')
cursor.execute('DROP TABLE IF EXISTS card_tribes;')
cursor.execute('DROP TABLE IF EXISTS card_sigils;')
cursor.execute('DROP TABLE IF EXISTS card_flags;')
cursor.execute('DROP TABLE IF EXISTS card_decals;')
cursor.execute('DROP TABLE IF EXISTS death_cards;')
cursor.execute('DROP TABLE IF EXISTS card_staticons;')

# CREATE TABLE statements
cursor.execute('''CREATE TABLE flags (
    name VARCHAR(45) PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE staticons (
    name VARCHAR(45) PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE decals (
    name VARCHAR(45),
    filename TEXT PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE notes (
    id INT PRIMARY KEY,
    description TEXT DEFAULT '',
    mechanics TEXT DEFAULT '',
    gmNotes TEXT DEFAULT ''
);''')

cursor.execute('''CREATE TABLE sigils (
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY,
    note_id INT, 
    FOREIGN KEY (note_id) REFERENCES notes (id)
);''')

cursor.execute(''' CREATE TABLE tribes (
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY,
    priority INT,
    note_id INT
);''')

cursor.execute('''CREATE TABLE cards (
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY,
    power INTEGER,
    health INTEGER,
    bloodCost INTEGER DEFAULT 0,
    boneCost INTEGER DEFAULT 0,
    energyCost INTEGER DEFAULT 0,
    orangeMoxCost INTEGER DEFAULT 0,
    greenMoxCost INTEGER DEFAULT 0,
    blueMoxCost INTEGER DEFAULT 0,
    rarity VARCHAR(10) CHECK (rarity IN ('common', 'rare', 'terrain', 'rareTerrain', 'spell')) NOT NULL,
    temple VARCHAR(10) CHECK (temple IN ('wizard', 'undead', 'tech', 'nature')) NOT NULL,
    note_id INT
);''')

cursor.execute('''CREATE TABLE death_cards(
    card_filename VARCHAR(45) PRIMARY KEY,
    head VARCHAR(10) NOT NULL,
    eyes INT NOT NULL,
    mouth INT NOT NULL,
    lost_eye VARCHAR(10) CHECK (lost_eye IN ('True', 'False')),
    FOREIGN KEY (card_filename) REFERENCES card (filename)
);''')

cursor.execute('''CREATE TABLE card_tribes (
    card_filename VARCHAR(45),
    tribe_filename VARCHAR(45),
    PRIMARY KEY (card_filename, tribe_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (tribe_filename) REFERENCES tribes (filename)
);''')

cursor.execute('''CREATE TABLE card_sigils (
    card_filename VARCHAR(45),
    sigil_filename VARCHAR(45),
    PRIMARY KEY (card_filename, sigil_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (sigil_filename) REFERENCES sigils (filename)
);''')

cursor.execute('''CREATE TABLE card_flags (
    card_filename VARCHAR(45),  
    flag_name INTEGER,          
    PRIMARY KEY (card_filename, flag_name),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (flag_name) REFERENCES flags (name)
);''')

cursor.execute('''CREATE TABLE card_staticons (
    card_filename VARCHAR(45),  
    staticon_name INTEGER,          
    PRIMARY KEY (card_filename, staticon_name),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (staticon_name) REFERENCES staticons (name)
);''')


cursor.execute('''CREATE TABLE card_decals (
    card_filename VARCHAR(45),  
    decal_filename INTEGER,     
    PRIMARY KEY (card_filename, decal_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (decal_filename) REFERENCES flags (filename)
);''')


# INSERT Statements
# Stat Icons
staticon_data = [
    ('ants',),
    ('sacrificesthisturn',),
    ('bell',),
    ('cardsinhand',),
    ('mirror',),
    ('bones',),
    ('greengems',)
]
for data in staticon_data:
    cursor.execute('INSERT INTO staticons (name) VALUES (?)', data)

# Flags
flag_data = [
    ('golden',),
    ('no_terrain_layout',),
    ('squid',),
    ('emission',),
    ('red_emission',),
    ('hide_power_and_health',),
    ('death_card',),
    ('no_portrait',),
]
for data in flag_data:
    cursor.execute('INSERT INTO flags (name) VALUES (?)', data)

# Decals
decal_data = [
    ('Blood', 'blood1'),
    ('Blood', 'blood2'),
    ('Blood', 'blood3'),
    ('Blood', 'blood4'),
    ('Paint', 'paint1'),
    ('Paint', 'paint2'),
    ('Paint', 'paint3'),
    ('Long Elk', 'snelk'),
    ('Vertebrae', 'snelk1'),
    ('Vertebrae', 'snelk2'),
    ('Vertebrae', 'snelk3'),
    ('Vertebrae', 'snelk4'),
    ('Vertebrae', 'snelk5'),
    ('Vertebrae', 'snelk6'),
    ('Smoke', 'smoke'),
    ('Hungry Child', 'child'),
    ('Fungus', 'fungus'),
    ('Stitches', 'stitches')
]
for data in decal_data:
    cursor.execute('INSERT INTO decals (name, filename) VALUES (?, ?)', data)

# Notes
note_data = [

]
for data in note_data:
    cursor.execute('INSERT INTO notes (id, description, mechanics, gmNotes) VALUES (?, ?, ?, ?)', data)

# Tribes
tribe_data = [
    ('Avian', 'bird', 1, None),
    ('Canine', 'canine', 2, None),
    ('Hooved', 'hooved', 3, None),
    ('Reptilian', 'reptile', 4, None),
    ('Insectoid', 'insect', 5, None)
]
for data in tribe_data:
    cursor.execute('INSERT INTO tribes (name, filename, priority, note_id) VALUES (?, ?, ?, ?)', data)

# Sigils
sigil_data = [
    ('Made of Stone', 'madeofstone', None),
    ('Rabbit Hole', 'drawrabbits', None),
    ('Bees Within', 'beesonhit', None),
    ('Sprinter', 'strafe', None),
    ('Touch of Death', 'deathtouch', None),
    ('Fledgling', 'evolve', None),
    ('Fledgling', 'evolve_1', None),
    ('Fledgling', 'evolve_2', None),
    ('Fledgling', 'evolve_3', None),
    ('Dam Builder', 'createdams', None),
    ('Hoarder', 'tutor', None),
    ('Burrower', 'whackamole', None),
    ('Fecundity', 'drawcopy', None),
    ('Loose Tail', 'tailonhit', None),
    ('Corpse Eater', 'corpseeater', None),
    ('Bone King', 'quadruplebones', None),
    ('Waterborne', 'submerge', None),
    ('Unkillable', 'drawcopyondeath', None),
    ('Sharp Quills', 'sharp', None),
    ('Hefty', 'strafepush', None),
    ('Rampager', 'strafeswap', None),
    ('Brood Parasite', 'createegg', None),
    ('Armored', 'deathshield', None),
    ('Double Strike', 'doublestrike', None),
    ('Morsel', 'morsel', None),
    ('Blood Lust', 'gainattackonkill', None),
    ('Scavenger', 'opponentbones', None),
    ('Finical Hatchling', 'hydraegg', None),
    ('Ant Spawner', 'drawant', None),
    ('Guardian', 'guarddog', None),
    ('Airborne', 'flying', None),
    ('Many Lives', 'sacrificial', None),
    ('Repulsive', 'preventattack', None),
    ('Worthy Sacrifice', 'tripleblood', None),
    ('Mighty Leap', 'reach', None),
    ('Bifurcated Strike', 'splitstrike', None),
    ('Trifurcated Strike', 'tristrike', None),
    ('Frozen Away', 'icecube', None),
    ('Sinkhole', 'sinkhole', None),
    ('Bone Digger', 'bonedigger', None),
    ('Trinket Bearer', 'randomconsumable', None),
    ('Steel Trap', 'steeltrap', None),
    ('Amorphous', 'randomability', None),
    ('Tidal Lock', 'squirrelorbit', None),
    ('Moon Strike', 'allstrike', None),
    ('Leader', 'buffneighbours', None),
    ('Brittle', 'brittle', None),
    ('Skeleton Crew', 'skeletonstrafe', None),
    ('Green Mox', 'gaingemgreen', None),
    ('Orange Mox', 'gaingemorange', None),
    ('Blue Mox', 'gaingemblue', None),
    ('Gem Animator', 'buffgems', None),
    ('Ruby Heart', 'droprubyondeath', None),
    ('Mental Gemnastics', 'gemsdraw', None),
    ('Gem Dependant', 'gemdependant', None),
    ('Great Mox', 'gaingemtriple', None),
    ('Handy', 'drawnewhand', None),
    ('Squirrel Shedder', 'squirrelstrafe', None),
    ('Attack Conduit', 'conduitbuffattack', None),
    ('Spawn Conduit', 'conduitfactory', None),
    ('Healing Conduit', 'conduitheal', None),
    ('Null Conduit', 'conduitnull', None),
    ('Battery Bearer', 'gainbattery', None),
    ('Detonator', 'explodeondeath', None),
    ('Sniper', 'sniper', None),
    ('Nano Armor', 'deathshield_nano', None),
    ('Overclocked', 'permadeath', None),
    ('Bomb Latch', 'latchexplodeondeath', None),
    ('Brittle Latch', 'latchbrittle', None),
    ('Shield Latch', 'latchdeathshield', None),
    ('Dead Byte', 'filesizedamage', None),
    ('Hostage File', 'deletefile', None),
    ('Transformer', 'transformer', None),
    ('Sentry', 'sentry', None),
    ('Gem Detonator', 'explodegems', None),
    ('Gem Guardian', 'shieldgems', None),
    ('Vessel Printer', 'drawvesselonhit', None),
    ('Energy Conduit', 'conduitenergy', None),
    ('Bomb Spewer', 'bombspawner', None),
    ('Double Death', 'doubledeath', None),
    ('Power Dice', 'activatedrandompowerenergy', None),
    ('Enlarge', 'activatedstatsup', None),
    ('Swapper', 'swapstats', None),
    ('Disentomb', 'activateddrawskeleton', None),
    ('Energy Gun', 'activateddealdamage', None),
    ('Bellist', 'createbells', None),
    ('Annoying', 'buffenemy', None),
    ('Gem Spawn Conduit', 'conduitspawngems', None),
    ('Gift Bearer', 'drawrandomcardondeath', None),
    ('Looter', 'loot', None),
    ('True Scholar', 'activatedsacrificedrawcards', None),
    ('Stimulate', 'activatedstatsupenergy', None),
    ('Marrow Sucker', 'activatedheal', None),
    ('Stinky', 'debuffenemy', None),
    ('Buff When Powered', 'cellbuffself', None),
    ('Gift When Powered', 'celldrawrandomcardondeath', None),
    ('Trifurcated When Powered', 'celltristrike', None),
    ('Bonehorn', 'activatedenergytobones', None),
    ('Clinger', 'movebeside', None),
    ('WaterborneSquid', 'submergesquid', None),
    ('Blood Guzzler', 'bloodguzzler', None),
    ('Haunter', 'haunter', None),
    ('Exploding Corpse', 'explodingcorpse', None),
    ('Apparition', 'bloodymary', None),
    ('Virtual Realist', 'virtualreality', None),
    ('Head of Edaxio', 'edaxiohead', None),
    ('Arms of Edaxio', 'edaxioarms', None),
    ('Legs of Edaxio', 'edaxiolegs', None),
    ('Torso of Edaxio', 'edaxiotorso', None)
]
for data in sigil_data:
    cursor.execute('INSERT INTO sigils (name, filename, note_id) VALUES (?, ?, ?)', data)

# Blood Cards
blood_card_data = [
    ('Adder', 'Adder', 1, 1, 2, 'common', 'nature', None),
    ('Amalgam', 'Amalgam', 3, 3, 2, 'rare', 'nature', None),
    ('Worker Ant', 'Ant', None, 2, 1, 'common', 'nature', None),
    ('Ant Queen', 'AntQueen', None, 3, 2, 'common', 'nature', None),
    ('Beaver', 'Beaver', 1, 4, 2, 'common', 'nature', None),
    ('Bee', 'Bee', 1, 1, None, 'common', 'nature', None),
    ('Beehive', 'Beehive', 0, 2, 1, 'common', 'nature', None),
    ('Bloodhound', 'Bloodhound', 2, 3, 2, 'common', 'nature', None),
    ('Boulder', 'Boulder', 0, 5, 0, 'common', 'nature', None),
    ('Bullfrog', 'Bullfrog', 1, 2, 1, 'common', 'nature', None),
    ('Caged Wolf', 'CagedWolf', 0, 6, 2, 'common', 'nature', None),
    ('Cat', 'Cat', 0, 1, 1, 'common', 'nature', None),
    ('Undead Cat', 'UndeadCat', 3, 6, 1, 'common', 'nature', None),
    ('The Daus', 'Daus', 2, 2, 2, 'common', 'nature', None),
    ('Elk', 'Elk', 2, 4, 2, 'common', 'nature', None),
    ('Elk Fawn', 'ElkFawn', 1, 1, 1, 'common', 'nature', None),
    ('Field Mice', 'FieldMice', 2, 2, 2, 'common', 'nature', None),
    ('Geck', 'Geck', 1, 1, None, 'common', 'nature', None),
    ('Black Goat', 'Goat', 0, 1, 1, 'common', 'nature', None),
    ('Black Goat', 'Goat_Sexy', 0, 1, 1, 'common', 'nature', None),
    ('Grizzly', 'Grizzly', 4, 6, 3, 'common', 'nature', None),
    ('Child 13', 'JerseyDevil', 0, 1, 1, 'common', 'nature', None),
    ('Child 13', 'JerseyDevil_Flying', 2, 1, 1, 'common', 'nature', None),
    ('Kingfisher', 'Kingfisher', 1, 1, 1, 'common', 'nature', None),
    ('Magpie', 'Magpie', 1, 1, 2, 'common', 'nature', None),
    ('Mantis', 'Mantis', 1, 1, 1, 'common', 'nature', None),
    ('Mantis God', 'MantisGod', 1, 1, 1, 'common', 'nature', None),
    ('Mole', 'Mole', 0, 4, 1, 'common', 'nature', None),
    ('Mole Man', 'MoleMan', 0, 6, 1, 'common', 'nature', None),
    ('Mole Seaman', 'MoleSeaman', 1, 8, 1, 'common', 'nature', None),
    ('Moose Buck', 'Moose', 3, 7, 3, 'common', 'nature', None),
    ('Strange Larva', 'Mothman_1', 0, 3, 1, 'common', 'nature', None),
    ('Strange Pupa', 'Mothman_2', 0, 3, 1, 'common', 'nature', None),
    ('Mothman', 'Mothman_3', 7, 3, 1, 'common', 'nature', None),
    ('Pack Mule', 'Mule', 0, 5, None, 'common', 'nature', None),
    ('River Otter', 'Otter', 1, 1, 1, 'common', 'nature', None),
    ('Ouroboros', 'Ouroboros', 1, 1, 2, 'common', 'nature', None),
    ('Pack Rat', 'PackRat', 2, 2, 2, 'common', 'nature', None),
    ('Porcupine', 'Porcupine', 1, 2, 1, 'common', 'nature', None),
    ('Pronghorn', 'Pronghorn', 1, 3, 2, 'common', 'nature', None),
    ('Rabbit', 'Rabbit', 0, 1, None, 'common', 'nature', None),
    ('Rat King', 'RatKing', 2, 1, 2, 'common', 'nature', None),
    ('Raven', 'Raven', 2, 3, 2, 'common', 'nature', None),
    ('Raven Egg', 'RavenEgg', 0, 2, 1, 'common', 'nature', None),
    ('Great White', 'Shark', 4, 2, 3, 'common', 'nature', None),
    ('Great White', 'Shark_Bloodless', 4, 2, 3, 'common', 'nature', None),
    ('Skink', 'Skink', 1, 2, 1, 'common', 'nature', None),
    ('Skunk', 'Skunk', 0, 3, 1, 'common', 'nature', None),
    ('River Snapper', 'Turtle', 1, 6, 2, 'common', 'nature', None),
    ('Sparrow', 'Sparrow', 1, 2, 1, 'common', 'nature', None),
    ('squid_bell', 'SquidBell', None, 3, 2, 'common', 'nature', None),
    ('squid_cards', 'SquidCards', None, 1, 1, 'common', 'nature', None),
    ('squid_mirror', 'SquidMirror', None, 3, 1, 'common', 'nature', None),
    ('Squirrel', 'Squirrel', 0, 1, None, 'common', 'nature', None),
    ('Stoat', 'Stoat_Talking', 1, 3, 1, 'common', 'nature', None),
    ('Stunted Wolf', 'Wolf_Talking', 2, 2, 1, 'common', 'nature', None),
    ('Wriggling Tail', 'Skink_Tail', 0, 2, None, 'common', 'nature', None),
    ('Tail Feathers', 'Bird_Tail', 0, 2, None, 'common', 'nature', None),
    ('Furry Tail', 'Canine_Tail', 0, 2, None, 'common', 'nature', None),
    ('Wriggling Leg', 'Insect_Tail', 0, 2, None, 'common', 'nature', None),
    ('Urayuli', 'Urayuli', 7, 7, 4, 'common', 'nature', None),
    ('Vertebrae', 'Vertebrae', 0, 1, 0, 'common', 'nature', None),
    ('Warren', 'Warren', 0, 2, 1, 'common', 'nature', None),
    ('Wolf', 'Wolf', 3, 2, 2, 'common', 'nature', None),
    ('Wolf Cub', 'WolfCub', 1, 1, 1, 'common', 'nature', None),
    ('Bait Bucket', 'BaitBucket', 0, 1, 0, 'common', 'nature', None),
    ('Broken Egg', 'BrokenEgg', 0, 1, 0, 'common', 'nature', None),
    ('Dam', 'Dam', 0, 2, 0, 'common', 'nature', None),
    ('Chime', 'DausBell', 0, 1, 0, 'common', 'nature', None),
    ('Gold Nugget', 'GoldNugget', 0, 2, 0, 'common', 'nature', None),
    ('Golden Pelt', 'Pelt_Golden', 0, 3, 0, 'common', 'nature', None),
    ('Rabbit Pelt', 'Pelt_Hare', 0, 1, 0, 'common', 'nature', None),
    ('Wolf Pelt', 'Pelt_Wolf', 0, 2, 0, 'common', 'nature', None),
    ('Ring Worm', 'RingWorm', 0, 1, 1, 'common', 'nature', None),
    ('Stoat', 'Stoat', 1, 2, 1, 'common', 'nature', None),
    ('The Smoke', 'Smoke', 0, 3, 0, 'common', 'nature', None),
    ('Greater Smoke', 'Smoke_Improved', 1, 3, 0, 'common', 'nature', None),
    ('Starvation', 'StarvingMan', None, None, 0, 'common', 'nature', None),
    ('Starvation', 'StarvingMan_Flight', None, None, 0, 'common', 'nature', None),
    ('Leaping Trap', 'Trap', 0, 1, 0, 'common', 'nature', None),
    ('Strange Frog', 'TrapFrog', 1, 2, 1, 'common', 'nature', None),
    ('Frozen Opossum', 'Frozen_Opossum', 0, 5, 0, 'common', 'nature', None),
    ('Snowy Fir', 'Tree_SnowCovered', 0, 4, 0, 'common', 'nature', None),
    ('Grand Fir', 'Tree', 0, 3, 0, 'common', 'nature', None),
    ('Hungry Child', 'Child', 0, 0, 0, 'common', 'nature', None),
    ('Stump', 'Stump', 0, 3, 0, 'common', 'nature', None),
    ('AquaSquirrel', 'AquaSquirrel', 0, 1, 0, 'common', 'nature', None),
    ('Skeleton Crew', 'SkeletonPirate', 2, 1, 0, 'common', 'nature', None),
    ('Zombie Parrot', 'SkeletonParrot', 2, 3, 0, 'common', 'nature', None),
    ('Wild Bull', 'Bull', 3, 2, 2, 'common', 'nature', None),
    ('Cuckoo', 'Cuckoo', 1, 1, 1, 'common', 'nature', None),
    ('Ijiraq', 'Ijiraq', 4, 1, None, 'common', 'nature', None),
    ('Flying Ant', 'AntFlying', None, 1, 1, 'common', 'nature', None),
    ('Mud Turtle', 'MudTurtle_Shelled', 2, 2, 2, 'common', 'nature', None),
    ('Mud Turtle', 'MudTurtle', 2, 2, 2, 'common', 'nature', None),
    ('Dire Wolf Pup', 'DireWolfCub', 1, 1, 2, 'common', 'nature', None),
    ('Dire Wolf', 'DireWolf', 2, 5, 3, 'common', 'nature', None),
    ('Raccoon', 'Raccoon', 1, 1, 1, 'common', 'nature', None),
    ('Lammergeier', 'Lammergeier', None, 4, 3, 'common', 'nature', None),
    ('Red Hart', 'RedHart', None, 2, 2, 'common', 'nature', None),
    ('Tadpole', 'Tadpole', 0, 1, None, 'common', 'nature', None),
    ('Pelt Lice', 'Lice', 1, 1, 4, 'common', 'nature', None),
    ('Hodag', 'Hodag', 1, 5, 2, 'common', 'nature', None),
    ('Great Kraken', 'Kraken', 1, 1, 1, 'common', 'nature', None),
    ('Louis', 'Louis', 1, 1, 1, 'common', 'nature', None),
    ('Kaycee', 'Kaycee', 1, 2, 1, 'common', 'nature', None)
]
for data in blood_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, bloodCost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# Bone Cards
bone_card_data = [
    ('Alpha', 'Alpha', 1, 2, 4, 'common', 'nature', None),
    ('Amoeba', 'Amoeba', 1, 2, 2, 'common', 'nature', None),
    ('Bat', 'Bat', 2, 1, 4, 'common', 'nature', None),
    ('Cockroach', 'Cockroach', 1, 1, 4, 'common', 'nature', None),
    ('Coyote', 'Coyote', 2, 1, 4, 'common', 'nature', None),
    ('Corpse Maggots', 'Maggots', 1, 2, 5, 'common', 'nature', None),
    ('Opossum', 'Opossum', 1, 1, 2, 'common', 'nature', None),
    ('Rattler', 'Rattler', 3, 1, 6, 'common', 'nature', None),
    ('Long Elk', 'LongElk', 1, 2, 4, 'common', 'nature', None),
    ('Stinkbug', 'Stinkbug_Talking', 1, 2, 2, 'common', 'nature', None),
    ('Turkey Vulture', 'Vulture', 3, 3, 8, 'common', 'nature', None),
    ('Mealworm', 'MealWorm', 0, 2, 2, 'common', 'nature', None),
    ('Wolverine', 'Wolverine', 1, 3, 5, 'common', 'nature', None),
    ('Curious Egg', 'HydraEgg', 0, 1, 1, 'common', 'nature', None),
    ('Hydra', 'Hydra', 1, 5, 1, 'common', 'nature', None),
    ('Reginald', 'Reginald', 1, 3, 3, 'common', 'nature', None),
    ('Kaminski', 'Kaminski', 0, 1, 1, 'common', 'nature', None)
]
for data in bone_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, boneCost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# Energy Cards
energy_card_data = [

]
for data in energy_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, boneCost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# (Orange, Green, Blue) Mox Cards
mox_card_data = [

]
for data in mox_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, orangeCost, greenCost, blueCost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# Multi-Cost Cards
# Will implement when needed

#Death Cards
death_card_data = [
    ('Reginald', 'settlerman', 3, 1, 'False' ),
    ('Louis', 'chief', 1, 3, 'False' ),
    ('Kaminski', 'settlerwoman', 2, 4, 'False' ),
    ('Kaycee', 'wildling', 5, 2, 'False')
]
for data in death_card_data:
    cursor.execute('INSERT INTO death_cards (card_filename, head, eyes, mouth, lost_eye) VALUES (?, ?, ?, ?, ?)', data)

# Card Tribes
card_tribe_data = [
    ('Adder', 'reptile'),
    ('Alpha', 'canine'),
    ('Amalgam', 'bird'),
    ('Amalgam', 'canine'),
    ('Amalgam', 'hooved'),
    ('Amalgam', 'insect'),
    ('Amalgam', 'reptile'),
    ('Ant', 'insect'),
    ('AntQueen', 'insect'),
    ('Bee', 'insect'),
    ('Beehive', 'insect'),
    ('Bloodhound', 'canine'),
    ('Bullfrog', 'reptile'),
    ('CagedWolf', 'canine'),
    ('Cockroach', 'insect'),
    ('Coyote', 'canine'),
    ('Elk', 'hooved'),
    ('ElkFawn', 'hooved'),
    ('Geck', 'reptile'),
    ('Goat', 'hooved'),
    ('Goat_Sexy', 'hooved'),
    ('JerseyDevil', 'hooved'),
    ('JerseyDevil_Flying', 'hooved'),
    ('Kingfisher', 'bird'),
    ('Maggots', 'insect'),
    ('Magpie', 'bird'),
    ('Mantis', 'insect'),
    ('MantisGod', 'insect'),
    ('Moose', 'hooved'),
    ('Mothman_1', 'insect'),
    ('Mothman_2', 'insect'),
    ('Mothman_3', 'insect'),
    ('Mule', 'hooved'),
    ('Ouroboros', 'reptile'),
    ('Pronghorn', 'hooved'),
    ('Rattler', 'reptile'),
    ('Raven', 'bird'),
    ('RavenEgg', 'bird'),
    ('Skink', 'reptile'),
    ('Turtle', 'reptile'),
    ('LongElk', 'hooved'),
    ('Sparrow', 'bird'),
    ('Stinkbug_Talking', 'insect'),
    ('Vulture', 'bird'),
    ('Vertebrae', 'hooved'),
    ('Wolf', 'canine'),
    ('WolfCub', 'canine'),
    ('RingWorm', 'insect'),
    ('Bull', 'hooved'),
    ('Cuckoo', 'bird'),
    ('AntFlying', 'insect'),
    ('MudTurtle_Shelled', 'reptile'),
    ('Mudturtle', 'reptile'),
    ('DireWolfCub', 'canine'),
    ('DireWolf', 'canine'),
    ('MealWorm', 'insect'),
    ('Lammergeier', 'bird'),
    ('RedHart', 'hooved'),
    ('Tadpole', 'reptile'),
    ('Lice', 'insect'),
    ('Hydra', 'bird'),
    ('Hydra', 'canine'),
    ('Hydra', 'hooved'),
    ('Hydra', 'insect'),
    ('Hydra', 'reptile')
]
for data in card_tribe_data:
    cursor.execute('INSERT INTO card_tribes (card_filename, tribe_filename) VALUES (?, ?)', data)

# Card Sigils
card_sigil_data = [
    ('Adder', 'deathtouch'),
    ('Alpha', 'buffneighbours'),
    ('Amoeba', 'randomability'),
    ('AntQueen', 'drawant'),
    ('Bat', 'flying'),
    ('Beaver', 'createdams'),
    ('Bee', 'flying'),
    ('Beehive', 'beesonhit'),
    ('Bloodhound', 'guarddog'),
    ('Boulder', 'madeofstone'),
    ('Bullfrog', 'reach'),
    ('Cat', 'sacrificial'),
    ('Cockroach', 'drawcopyondeath'),
    ('Daus', 'createbells'),
    ('Deer', 'strafe'),
    ('DeerCub', 'strafe'),
    ('DeerCub', 'evolve_1'),
    ('FieldMice', 'drawcopy'),
    ('Goat', 'tripleblood'),
    ('Goat_Sexy', 'tripleblood'),
    ('JerseyDevil', 'sacrificial'),
    ('JerseyDevil_Flying', 'sacrificial'),
    ('JerseyDevil_Flying', 'flying'),
    ('Kingfisher', 'flying'),
    ('Kingfisher', 'submerge'),
    ('Maggots', 'corpseeater'),
    ('Magpie', 'flying'),
    ('Magpie', 'tutor'),
    ('Mantis', 'splitstrike'),
    ('MantisGod', 'tristrike'),
    ('Mole', 'whackamole'),
    ('MoleMan', 'whackamole'),
    ('MoleMan', 'reach'),
    ('MoleSeaman', 'whackamole'),
    ('MoleSeaman', 'reach'),
    ('Moose', 'strafepush'),
    ('Mothman_1', 'evolve_1'),
    ('Mothman_2', 'evolve_1'),
    ('Mothman_3', 'flying'),
    ('Mule', 'strafe'),
    ('Otter', 'submerge'),
    ('Ouroboros', 'drawcopyondeath'),
    ('Pack Rat', 'randomconsumable'),
    ('Porcupine', 'sharp'),
    ('Pronghorn', 'strafe'),
    ('Pronghorn', 'splitstrike'),
    ('RatKing', 'quadruplebones'),
    ('Raven', 'flying'),
    ('RavenEgg', 'evolve_1'),
    ('Shark', 'submerge'),
    ('Shark_Bloodless', 'submerge'),
    ('Skink', 'tailonhit'),
    ('Skunk', 'debuffenemy'),
    ('LongElk', 'strafe'),
    ('LongElk', 'deathtouch'),
    ('Sparrow', 'flying'),
    ('Stinkbug_Talking', 'debuffenemy'),
    ('Vulture', 'flying'),
    ('Warren', 'drawrabbits'),
    ('WolfCub', 'evolve_1'),
    ('Smoke', 'quadruplebones'),
    ('Smoke_Improved', 'quadruplebones'),
    ('StarvingMan', 'preventattack'),
    ('StarvingMan_Flight', 'preventattack'),
    ('StarvingMan_Flight', 'flying'),
    ('Trap', 'reach'),
    ('Trap', 'steeltrap'),
    ('TrapFrog', 'reach'),
    ('Frozen_Opossum', 'icecube'),
    ('Tree_SnowCovered', 'reach'),
    ('Tree', 'reach'),
    ('AquaSquirrel', 'submerge'),
    ('SkeletonPirate', 'brittle'),
    ('SkeletonParrot', 'flying'),
    ('SkeletonParrot', 'brittle'),
    ('Bull', 'strafeswap'),
    ('Cuckoo', 'flying'),
    ('Cuckoo', 'createegg'),
    ('Ijiraq', 'preventattack'),
    ('AntFlying', 'flying'),
    ('MudTurtle_Shelled', 'deathshield'),
    ('DireWolfCub', 'bonedigger'),
    ('DireWolfCub', 'evolve_1'),
    ('DireWolf', 'doublestrike'),
    ('MealWorm', 'morsel'),
    ('Wolverine', 'gainattackonkill'),
    ('Raccoon', 'opponentbones'),
    ('Lammergeier', 'flying'),
    ('RedHart', 'strafe'),
    ('Tadpole', 'submerge'),
    ('Tadpole', 'evolve_1'),
    ('Lice', 'doublestrike'),
    ('Hodag', 'gainattackonkill'),
    ('Kraken', 'submergesquid'),
    ('HydraEgg', 'hydraegg'),
    ('Hydra', 'splitstrike'),
    ('Hydra', 'tristrike'),
    ('Reginald', 'deathtouch'),
    ('Louis', 'strafe'),
    ('Louis', 'submerge'),
    ('Kaminski', 'guarddog'),
    ('Kaminski', 'sharp'),
    ('Kaycee', 'splitstrike'),
    ('Kaycee', 'sharp')
]
for data in card_sigil_data:
    cursor.execute('INSERT INTO card_sigils (card_filename, sigil_filename) VALUES (?, ?)', data)

# Card Flags
card_flag_data = [
    ('SquidBell', 'squid'),
    ('SquidCards', 'squid'),
    ('SquidMirror', 'squid'),
    ('Gold Nugget', 'golden'),
    ('Gold Nugget', 'emission'),
    ('Pelt_Golden', 'golden'),
    ('Pelt_Golden', 'emission'),
    ('Smoke_Improved', 'emission'),
    ('StarvingMan', 'hide_power_and_health'),
    ('StarvingMan_Flight', 'hide_power_and_health'),
    ('Reginald', 'death_card'),
    ('Louis', 'death_card'),
    ('Kaminski', 'death_card'),
    ('Kaycee', 'death_card'),
    ('Vertebrae', 'no_portrait'),
    ('LongElk', 'no_portrait'),
    ('Child', 'no_portrait')
]
for data in card_flag_data:
    cursor.execute('INSERT INTO card_flags (card_filename, flag_name) VALUES (?, ?)', data)

# Card Staticons
card_staticon_data = [
    ('Ant', 'ants'),
    ('Ant Queen', 'ants'),
    ('SquidBell', 'bell'),
    ('SquidCards', 'cardsinhand'),
    ('SquidMirror', 'mirror'),
    ('AntFlying', 'ants'),
    ('Lammergeier', 'bones'),
    ('Red Hart', 'sacrificesthisturn'),
]
for data in card_staticon_data:
    cursor.execute('INSERT INTO card_staticons (card_filename, staticon_name) VALUES (?, ?)', data)

# Card Decals
card_decal_data = [
    ('BaitBucket', 'blood2'),
    ('Shark', 'blood2'),
    ('Smoke', 'smoke'),
    ('Smoke_Improved', 'smoke'),
    ('Child', 'child'),
    ('LongElk', 'snelk')
]
for data in card_decal_data:
    cursor.execute('INSERT INTO card_decals (card_filename, decal_filename) VALUES (?, ?)', data)

# Commit and disconnect
conn.commit()
conn.close()

print("Database 'inscryption.db' initialized.")
