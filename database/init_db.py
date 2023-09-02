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
    filename VARCHAR(45),
    note_id INT, 
    PRIMARY KEY (name, filename)
    FOREIGN KEY (note_id) REFERENCES notes (id)
);''')

cursor.execute(''' CREATE TABLE tribes (
    name VARCHAR(45),
    filename VARCHAR(45),
    priority INT,
    note_id INT,
    PRIMARY KEY (name, filename)
);''')

cursor.execute('''CREATE TABLE cards (
    name VARCHAR(45),
    filename VARCHAR(45),
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
    note_id INT,
    PRIMARY KEY (name, filename)
);''')

cursor.execute('''CREATE TABLE death_cards(
    card_name VARCHAR(45),
    card_filename VARCHAR(45),
    head VARCHAR(10) NOT NULL,
    eyes INT NOT NULL,
    mouth INT NOT NULL,
    lost_eye VARCHAR(10) CHECK (lost_eye IN ('True', 'False')),
    PRIMARY KEY(card_name, card_filename),
    FOREIGN KEY (card_name) REFERENCES card (name),
    FOREIGN KEY (card_filename) REFERENCES card (filename)
);''')

cursor.execute('''CREATE TABLE card_tribes (
    card_name VARCHAR(45),
    card_filename VARCHAR(45),
    tribe_name VARCHAR(45),
    tribe_filename VARCHAR(45),
    PRIMARY KEY (card_name, card_filename, tribe_name, tribe_filename),
    FOREIGN KEY (card_name) REFERENCES card (name),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (tribe_name) REFERENCES tribes (name),
    FOREIGN KEY (tribe_filename) REFERENCES tribes (filename)
);''')

cursor.execute('''CREATE TABLE card_sigils (
    card_name VARCHAR(45),
    card_filename VARCHAR(45),
    sigil_name VARCHAR(45),
    sigil_filename VARCHAR(45),
    PRIMARY KEY (card_name, card_filename, sigil_name, sigil_filename),
    FOREIGN KEY (card_name) REFERENCES card (name),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (sigil_name) REFERENCES card (name),
    FOREIGN KEY (sigil_filename) REFERENCES sigils (filename)
);''')

cursor.execute('''CREATE TABLE card_flags (
    card_name VARCHAR(45),
    card_filename VARCHAR(45),  
    flag_name INTEGER,          
    PRIMARY KEY (card_name, card_filename, flag_name),
    FOREIGN KEY (card_name) REFERENCES card (name),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (flag_name) REFERENCES flags (name)
);''')

cursor.execute('''CREATE TABLE card_staticons (
    card_name VARCHAR(45),
    card_filename VARCHAR(45),  
    staticon_name INTEGER,          
    PRIMARY KEY (card_name, card_filename, staticon_name),
    FOREIGN KEY (card_name) REFERENCES card (name),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (staticon_name) REFERENCES staticons (name)
);''')


cursor.execute('''CREATE TABLE card_decals (
    card_name VARCHAR(45),
    card_filename VARCHAR(45),  
    decal_filename INTEGER,     
    PRIMARY KEY (card_name, card_filename, decal_filename),
    FOREIGN KEY (card_name) REFERENCES card (name),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (decal_filename) REFERENCES flags (filename)
);''')


# INSERT Statements
# Flags
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

flag_data = [
    ('golden',),
    ('no_terrain_layout',),
    ('squid',),
    ('emission',),
    ('red_emission',),
    ('hide_power_and_health',),
    ('death_card',),
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
    ('Nano Armor', 'deathshield', None),
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
    ('Undead Cat', 'CatUndead', 3, 6, 1, 'common', 'nature', None),
    ('The Daus', 'Daus', 2, 2, 2, 'common', 'nature', None),
    ('Elk', 'Elk', 2, 4, 2, 'common', 'nature', None),
    ('Elk Fawn', 'ElkCub', 1, 1, 1, 'common', 'nature', None),
    ('Field Mice', 'FieldMouse', 2, 2, 2, 'common', 'nature', None),
    ('Geck', 'Geck', 1, 1, None, 'common', 'nature', None),
    ('Black Goat', 'Goat', 0, 1, 1, 'common', 'nature', None),
    ('Black Goat', 'GoatSexy', 0, 1, 1, 'common', 'nature', None),
    ('Grizzly', 'Grizzly', 4, 6, 3, 'common', 'nature', None),
    ('Child 13', 'JerseyDevil', 0, 1, 1, 'common', 'nature', None),
    ('Child 13', 'JerseyDevilFlying', 2, 1, 1, 'common', 'nature', None),
    ('Kingfisher', 'Kingfisher', 1, 1, 1, 'common', 'nature', None),
    ('Magpie', 'Magpie', 1, 1, 2, 'common', 'nature', None),
    ('Mantis', 'Mantis', 1, 1, 1, 'common', 'nature', None),
    ('Mantis God', 'MantisGod', 1, 1, 1, 'common', 'nature', None),
    ('Mole', 'Mole', 0, 4, 1, 'common', 'nature', None),
    ('Mole Man', 'MoleMan', 0, 6, 1, 'common', 'nature', None),
    ('Mole Seaman', 'MoleSeaman', 1, 8, 1, 'common', 'nature', None),
    ('Moose Buck', 'Moose', 3, 7, 3, 'common', 'nature', None),
    ('Strange Larva', 'Mothman_Stage1', 0, 3, 1, 'common', 'nature', None),
    ('Strange Pupa', 'Mothman_Stage2', 0, 3, 1, 'common', 'nature', None),
    ('Mothman', 'Mothman_Stage3', 7, 3, 1, 'common', 'nature', None),
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
    ('Great White_Bloodless', 'Shark', 4, 2, 3, 'common', 'nature', None),
    ('Skink', 'Skink', 1, 2, 1, 'common', 'nature', None),
    ('Skunk', 'Skunk', 0, 3, 1, 'common', 'nature', None),
    ('River Snapper', 'Snapper', 1, 6, 2, 'common', 'nature', None),
    ('Sparrow', 'Sparrow', 1, 2, 1, 'common', 'nature', None),
    ('squid_bell', 'SquidBell', None, 3, 2, 'common', 'nature', None),
    ('squid_cards', 'SquidCards', None, 1, 1, 'common', 'nature', None),
    ('squid_mirror', 'SquidMirror', None, 3, 1, 'common', 'nature', None),
    ('Squirrel', 'Squirrel', 0, 1, None, 'common', 'nature', None),
    ('Stoat', 'Stoat_Talking', 1, 3, 1, 'common', 'nature', None),
    ('Stunted Wolf', 'Wolf_Talking', 2, 2, 1, 'common', 'nature', None),
    ('Wriggling Tail', 'SkinkTail', 0, 2, None, 'common', 'nature', None),
    ('Tail Feathers', 'Tail_Bird', 0, 2, None, 'common', 'nature', None),
    ('Furry Tail', 'Tail_Furry', 0, 2, None, 'common', 'nature', None),
    ('Wriggling Leg', 'Tail_Insect', 0, 2, None, 'common', 'nature', None),
    ('Urayuli', 'Urayuli', 7, 7, 4, 'common', 'nature', None),
    ('Vertabrae', 'Vertabrae', 0, 1, 0, 'common', 'nature', None),
    ('Warren', 'Warren', 0, 2, 1, 'common', 'nature', None),
    ('Wolf', 'Wolf', 3, 2, 2, 'common', 'nature', None),
    ('Wolf Cub', 'WolfCub', 1, 1, 1, 'common', 'nature', None),
    ('Bait Bucket', 'BaitBucket', 0, 1, 0, 'common', 'nature', None),
    ('Broken Egg', 'BrokenEgg', 0, 1, 0, 'common', 'nature', None),
    ('Dam', 'Dam', 0, 2, 0, 'common', 'nature', None),
    ('Chime', 'DausBell', 0, 1, 0, 'common', 'nature', None),
    ('Gold Nugget', 'GoldNugget', 0, 2, 0, 'common', 'nature', None),
    ('Golden Pelt', 'PeltGolden', 0, 3, 0, 'common', 'nature', None),
    ('Rabbit Pelt', 'PeltHare', 0, 1, 0, 'common', 'nature', None),
    ('Wolf Pelt', 'PeltWolf', 0, 2, 0, 'common', 'nature', None),
    ('Ring Worm', 'RingWorm', 0, 1, 1, 'common', 'nature', None),
    ('Stoat', 'Stoat', 1, 2, 1, 'common', 'nature', None),
    ('The Smoke', 'Smoke', 0, 3, 0, 'common', 'nature', None),
    ('Greater Smoke', 'Smoke_Improved', 1, 3, 0, 'common', 'nature', None),
    ('Starvation', 'Starvation', None, None, 0, 'common', 'nature', None),
    ('Starvation_Flight', 'Starvation', None, None, 0, 'common', 'nature', None),
    ('Leaping Trap', 'Trap', 0, 1, 0, 'common', 'nature', None),
    ('Strange Frog', 'TrapFrog', 1, 2, 1, 'common', 'nature', None),
    ('Frozen Opossum', 'FrozenOpossum', 0, 5, 0, 'common', 'nature', None),
    ('Snowy Fir', 'Tree_SnowCovered', 0, 4, 0, 'common', 'nature', None),
    ('Grand Fir', 'Tree', 0, 3, 0, 'common', 'nature', None),
    ('Hungry Child', 'HungryChild', 0, 0, 0, 'common', 'nature', None),
    ('Stump', 'Stump', 0, 3, 0, 'common', 'nature', None),
    ('AquaSquirrel', 'AquaSquirrel', 0, 1, 0, 'common', 'nature', None),
    ('Skeleton Crew', 'SkeletonPirate', 2, 1, 0, 'common', 'nature', None),
    ('Zombie Parrot', 'SkeletonParrot', 2, 3, 0, 'common', 'nature', None),
    ('Wild Bull', 'Bull', 3, 2, 2, 'common', 'nature', None),
    ('Cuckoo', 'Cuckoo', 1, 1, 1, 'common', 'nature', None),
    ('Ijiraq', 'Ijiraq', 4, 1, None, 'common', 'nature', None),
    ('Flying Ant', 'AntFlying', None, 1, 1, 'common', 'nature', None),
    ('Mud Turtle', 'MudTurtleShelled', 2, 2, 2, 'common', 'nature', None),
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
    ('Reginald', 'Reginald', 'settlerman', 3, 1, 'False' ),
    ('Louis', 'Louis', 'chief', 1, 3, 'False' ),
    ('Kaminski', 'Kaminski', 'settlerwoman', 2, 4, 'False' ),
    ('Kaycee', 'Kaycee', 'wildling', 5, 2, 'False')
]
for data in death_card_data:
    cursor.execute('INSERT INTO death_cards (card_name, card_filename, head, eyes, mouth, lost_eye) VALUES (?, ?, ?, ?, ?, ?)', data)

# Card Tribes
card_tribe_data = [
    ('Adder', 'Adder', 'Reptilian', 'reptile'),
    ('Alpha', 'Alpha', 'Canine', 'canine'),
    ('Amalgam', 'Amalgam', 'Avian', 'bird'),
    ('Amalgam', 'Amalgam', 'Canine', 'canine'),
    ('Amalgam', 'Amalgam', 'Hooved', 'hooved'),
    ('Amalgam', 'Amalgam', 'Reptilian', 'insect'),
    ('Amalgam', 'Amalgam', 'Reptilian', 'reptile'),
    ('Worker Ant', 'Ant', 'Insectoid', 'insect'),
    ('Ant Queen', 'AntQueen', 'Insectoid', 'insect'),
    ('Bee', 'Bee', 'Insectoid', 'insect'),
    ('Beehive', 'Beehive', 'Insectoid', 'insect'),
    ('Bloodhound', 'Bloodhound', 'Canine', 'canine'),
    ('Bullfrog', 'Bullfrog', 'Reptilian', 'reptile'),
    ('Caged Wolf', 'CagedWolf', 'Canine', 'canine'),
    ('Cockroach', 'Cockroach', 'Insectoid', 'insect'),
    ('Coyote', 'Coyote', 'Canine', 'canine'),
    ('Elk', 'Elk', 'Hooved', 'hooved'),
    ('Elk Fawn', 'ElkCub', 'Hooved', 'hooved'),
    ('Geck', 'Geck', 'Reptilian', 'reptile'),
    ('Black Goat', 'Goat', 'Hooved', 'hooved'),
    ('Black Goat', 'GoatSexy', 'Hooved', 'hooved'),
    ('Child 13', 'JerseyDevil', 'Hooved', 'hooved'),
    ('Child 13', 'JerseyDevilFlying', 'Hooved', 'hooved'),
    ('Kingfisher', 'Kingfisher', 'Avian', 'bird'),
    ('Corpse Maggots', 'Maggots', 'Insectoid', 'insect'),
    ('Magpie', 'Magpie', 'Avian', 'bird'),
    ('Mantis', 'Mantis', 'Insectoid', 'insect'),
    ('Mantis God', 'MantisGod', 'Insectoid', 'insect'),
    ('Moose Buck', 'Moose', 'Hooved', 'hooved'),
    ('Strange Larva', 'Mothman_Stage1', 'Insectoid', 'insect'),
    ('Strange Pupa', 'Mothman_Stage2', 'Insectoid', 'insect'),
    ('Mothman', 'Mothman_Stage3', 'Insectoid', 'insect'),
    ('Pack Mule', 'Mule', 'Hooved', 'hooved'),
    ('Ouroboros', 'Ouroboros', 'Reptilian', 'reptile'),
    ('Pronghorn', 'Pronghorn', 'Hooved', 'hooved'),
    ('Rattler', 'Rattler', 'Reptilian', 'reptile'),
    ('Raven', 'Raven', 'Avian', 'bird'),
    ('Raven Egg', 'RavenEgg', 'Avian', 'bird'),
    ('Skink', 'Skink', 'Reptilian', 'reptile'),
    ('River Snapper', 'Snapper', 'Reptilian', 'reptile'),
    ('Long Elk', 'LongElk', 'Hooved', 'hooved'),
    ('Sparrow', 'Sparrow', 'Avian', 'bird'),
    ('Stinkbug', 'Stinkbug_Talking', 'Insectoid', 'insect'),
    ('Turkey Vulture', 'Vulture', 'Avian', 'bird'),
    ('Vertabrae', 'Vertabrae', 'Hooved', 'hooved'),
    ('Wolf', 'Wolf', 'Canine', 'canine'),
    ('Wolf Cub', 'WolfCub', 'Canine', 'canine'),
    ('Ring Worm', 'RingWorm', 'Insectoid', 'insect'),
    ('Wild Bull', 'Bull', 'Hooved', 'hooved'),
    ('Cuckoo', 'Cuckoo', 'Avian', 'bird'),
    ('Flying Ant', 'AntFlying', 'Insectoid', 'insect'),
    ('Mud Turtle', 'MudTurtleShelled', 'Reptilian', 'reptile'),
    ('Mud Turtle', 'MudTurtle', 'Reptilian', 'reptile'),
    ('Dire Wolf Pup', 'DireWolfCub', 'Canine', 'canine'),
    ('Dire Wolf', 'DireWolf', 'Canine', 'canine'),
    ('Mealworm', 'MealWorm', 'Insectoid', 'insect'),
    ('Lammergeier', 'Lammergeier', 'Avian', 'bird'),
    ('Red Hart', 'RedHart', 'Hooved', 'hooved'),
    ('Tadpole', 'Tadpole', 'Reptilian', 'reptile'),
    ('Pelt Lice', 'Lice', 'Insectoid', 'insect'),
    ('Hydra', 'Hydra', 'Avian', 'bird'),
    ('Hydra', 'Hydra', 'Canine', 'canine'),
    ('Hydra', 'Hydra', 'Hooved', 'hooved'),
    ('Hydra', 'Hydra', 'Insectoid', 'insect'),
    ('Hydra', 'Hydra', 'Reptilian', 'reptile')
]
for data in card_tribe_data:
    cursor.execute('INSERT INTO card_tribes (card_name, card_filename, tribe_name, tribe_filename) VALUES (?, ?, ?, ?)', data)

# Card Sigils
card_sigil_data = [
    ('Adder', 'Adder', 'Touch of Death', 'deathtouch'),
    ('Alpha', 'Alpha', 'Leader', 'buffneighbours'),
    ('Amoeba', 'Amoeba', 'Amorphous', 'randomability'),
    ('Ant Queen', 'AntQueen', 'Ant Spawner', 'drawant'),
    ('Bat', 'Bat', 'Airborne', 'flying'),
    ('Beaver', 'Beaver', 'Dam Builder', 'createdams'),
    ('Bee', 'Bee', 'Airborne', 'flying'),
    ('Beehive', 'Beehive', 'Bees Within', 'beesonhit'),
    ('Bloodhound', 'Bloodhound', 'Guardian', 'guarddog'),
    ('Boulder', 'Boulder', 'Made of Stone', 'madeofstone'),
    ('Bullfrog', 'Bullfrog', 'Mighty Leap', 'reach'),
    ('Cat', 'Cat', 'ManyLives', 'sacrificial'),
    ('Cockroach', 'Cockroach', 'Unkillable', 'drawcopyondeath'),
    ('The Daus', 'Daus', 'Bellist', 'createbells'),
    ('Elk', 'Elk', 'Sprinter', 'strafe'),
    ('Elk Fawn', 'ElkCub', 'Sprinter', 'strafe'),
    ('Elk Fawn', 'ElkCub', 'Fledgling', 'evolve_1'),
    ('Field Mice', 'FieldMouse', 'Fecundity', 'drawcopy'),
    ('Black Goat', 'Goat', 'Worthy Sacrifice', 'tripleblood'),
    ('Black Goat', 'GoatSexy', 'Worthy Sacrifice', 'tripleblood'),
    ('Child 13', 'JerseyDevil', 'Many Lives', 'sacrificial'),
    ('Child 13', 'JerseyDevilFlying', 'Many Lives', 'sacrificial'),
    ('Child 13', 'JerseyDevilFlying', 'Airborne', 'flying'),
    ('Kingfisher', 'Kingfisher', 'Airborne', 'flying'),
    ('Kingfisher', 'Kingfisher', 'Waterborne', 'submerge'),
    ('Corpse Maggots', 'Maggots', 'Corpse Eater', 'corpseeater'),
    ('Magpie', 'Magpie', 'Airborne', 'flying'),
    ('Magpie', 'Magpie', 'Hoarder', 'tutor'),
    ('Mantis', 'Mantis', 'Bifurcated Strike', 'splitstrike'),
    ('Mantis God', 'MantisGod', 'Trifurcated Strike', 'tristrike'),
    ('Mole', 'Mole', 'Burrower', 'whackamole'),
    ('Mole Man', 'MoleMan', 'Burrower', 'whackamole'),
    ('Mole Man', 'MoleMan', 'Mighty Leap', 'reach'),
    ('Mole Seaman', 'MoleSeaman', 'Burrower', 'whackamole'),
    ('Mole Seaman', 'MoleSeaman', 'Mighty Leap', 'reach'),
    ('Moose Buck', 'Moose', 'Hefty', 'strafepush'),
    ('Strange Larva', 'Mothman_Stage1', 'Fledgling', 'evolve_1'),
    ('Strange Pupa', 'Mothman_Stage2', 'Fledgling', 'evolve_1'),
    ('Mothman', 'Mothman_Stage3', 'Airborne', 'flying'),
    ('Pack Mule', 'Mule', 'Sprinter', 'strafe'),
    ('River Otter', 'Otter', 'Waterborne', 'submerge'),
    ('Ouroboros', 'Ouroboros', 'Unkillable', 'drawcopyondeath'),
    ('Pack Rat', 'Pack Rat', 'Trinket Bearer', 'randomconsumable'),
    ('Porcupine', 'Porcupine', 'Sharp Quills', 'sharp'),
    ('Pronghorn', 'Pronghorn', 'Sprinter', 'strafe'),
    ('Pronghorn', 'Pronghorn', 'Bifurcated Strike', 'splitstrike'),
    ('Rat King', 'RatKing', 'Bone King', 'quadruplebones'),
    ('Raven', 'Raven', 'Airborne', 'flying'),
    ('Raven Egg', 'RavenEgg', 'Fledgling', 'evolve_1'),
    ('Great White', 'Shark', 'Waterborne', 'submerge'),
    ('Great White_Bloodless', 'Shark', 'Waterborne', 'submerge'),
    ('Skink', 'Skink', 'Loose Tail', 'tailonhit'),
    ('Skunk', 'Skunk', 'Stinky', 'debuffenemy'),
    ('Long Elk', 'LongElk', 'Sprinter', 'strafe'),
    ('Long Elk', 'LongElk', 'Touch of Death', 'deathtouch'),
    ('Sparrow', 'Sparrow', 'Airborne', 'flying'),
    ('Stinkbug', 'Stinkbug_Talking', 'Stinky', 'debuffenemy'),
    ('Turkey Vulture', 'Vulture', 'Airborne', 'flying'),
    ('Warren', 'Warren', 'Rabbit Hole', 'drawrabbits'),
    ('Wolf Cub', 'WolfCub', 'Fledgling', 'evolve_1'),
    ('The Smoke', 'Smoke', 'Bone King', 'quadruplebones'),
    ('Greater Smoke', 'Smoke_Improved', 'Bone King', 'quadruplebones'),
    ('Starvation', 'Starvation', 'Repulsive', 'preventattack'),
    ('Starvation_Flight', 'Starvation', 'Repulsive', 'preventattack'),
    ('Starvation_Flight', 'Starvation', 'Airborne', 'flying'),
    ('Leaping Trap', 'Trap', 'Mighty Leap', 'reach'),
    ('Leaping Trap', 'Trap', 'Steel Trap', 'steeltrap'),
    ('Strange Frog', 'TrapFrog', 'Mighty Leap', 'reach'),
    ('Frozen Opossum', 'FrozenOpossum', 'Frozen Away', 'icecube'),
    ('Snowy Fir', 'Tree_SnowCovered', 'Mighty Leap', 'reach'),
    ('Grand Fir', 'Tree', 'Mighty Leap', 'reach'),
    ('AquaSquirrel', 'AquaSquirrel', 'Waterborne', 'submerge'),
    ('Skeleton Crew', 'SkeletonPirate', 'Brittle', 'brittle'),
    ('Zombie Parrot', 'SkeletonParrot', 'Airborne', 'flying'),
    ('Zombie Parrot', 'SkeletonParrot', 'Brittle', 'brittle'),
    ('Wild Bull', 'Bull', 'Rampager', 'strafeswap'),
    ('Cuckoo', 'Cuckoo', 'Airborne', 'flying'),
    ('Cuckoo', 'Cuckoo', 'Brood Parasite', 'createegg'),
    ('Ijiraq', 'Ijiraq', 'Repulsive', 'preventattack'),
    ('Flying Ant', 'AntFlying', 'Airborne', 'flying'),
    ('Mud Turtle', 'MudTurtleShelled', 'Armored', 'deathshield'),
    ('Dire Wolf Pup', 'DireWolfCub', 'Bone Digger', 'bonedigger'),
    ('Dire Wolf Pup', 'DireWolfCub', 'Fledgling', 'evolve_1'),
    ('Dire Wolf', 'DireWolf', 'Double Strike', 'doublestrike'),
    ('Mealworm', 'MealWorm', 'Morsel', 'morsel'),
    ('Wolverine', 'Wolverine', 'Blood Lust', 'gainattackonkill'),
    ('Raccoon', 'Raccoon', 'Scavenger', 'opponentbones'),
    ('Lammergeier', 'Lammergeier', 'Airborne', 'flying'),
    ('Red Hart', 'RedHart', 'Sprinter', 'strafe'),
    ('Tadpole', 'Tadpole', 'Waterborne', 'submerge'),
    ('Tadpole', 'Tadpole', 'Fledgling', 'evolve_1'),
    ('Pelt Lice', 'Lice', 'Double Strike', 'doublestrike'),
    ('Hodag', 'Hodag', 'Blood Lust', 'gainattackonkill'),
    ('Great Kraken', 'Kraken', 'WaterborneSquid', 'submergesquid'),
    ('Curious Egg', 'HydraEgg', 'Finical Hatchling', 'hydraegg'),
    ('Hydra', 'Hydra', 'Bifurcated Strike', 'splitstrike'),
    ('Hydra', 'Hydra', 'Trifurcated Strike', 'tristrike'),
    ('Reginald', 'Reginald', 'Touch of Death', 'deathtouch'),
    ('Louis', 'Louis', 'Sprinter', 'strafe'),
    ('Louis', 'Louis', 'Waterborne', 'submerge'),
    ('Kaminski', 'Kaminski', 'Guardian', 'guarddog'),
    ('Kaminski', 'Kaminski', 'Sharp Quills', 'sharp'),
    ('Kaycee', 'Kaycee', 'Bifurcated Strike', 'splitstrike'),
    ('Kaycee', 'Kaycee', 'Sharp Quills', 'sharp')
]
for data in card_sigil_data:
    cursor.execute('INSERT INTO card_sigils (card_name, card_filename, sigil_name, sigil_filename) VALUES (?, ?, ?, ?)', data)

# Card Flags
card_flag_data = [
    ('squid_bell', 'SquidBell', 'squid'),
    ('squid_cards', 'SquidCards', 'squid'),
    ('squid_mirror', 'SquidMirror', 'squid'),
    ('Gold Nugget', 'Gold Nugget', 'golden'),
    ('Gold Nugget', 'Gold Nugget', 'emission'),
    ('Golden Pelt', 'PeltGolden', 'golden'),
    ('Golden Pelt', 'PeltGolden', 'emission'),
    ('Greater Smoke', 'Smoke_Improved', 'emission'),
    ('Starvation', 'Starvation', 'hide_power_and_health'),
    ('Starvation_Flight', 'Starvation', 'hide_power_and_health'),
    ('Reginald', 'Reginald', 'death_card'),
    ('Louis', 'Louis', 'death_card'),
    ('Kaminski', 'Kaminski', 'death_card'),
    ('Kaycee', 'Kaycee', 'death_card')
]
for data in card_flag_data:
    cursor.execute('INSERT INTO card_flags (card_name, card_filename, flag_name) VALUES (?, ?, ?)', data)

# Card Staticons
card_staticon_data = [
    ('Worker Ant', 'Ant', 'ants'),
    ('Ant Queen', 'Ant Queen', 'ants'),
    ('squid_bell', 'SquidBell', 'bell'),
    ('squid_cards', 'SquidCards', 'cardsinhand'),
    ('squid_mirror', 'SquidMirror', 'mirror'),
    ('Flying Ant', 'AntFlying', 'ants'),
    ('Lammergeier', 'Lammergeier', 'bones'),
    ('Red Hart', 'Red Hart', 'sacrificesthisturn'),
]
for data in card_flag_data:
    cursor.execute('INSERT INTO card_staticons (card_name, card_filename, staticon_name) VALUES (?, ?, ?)', data)

# Card Decals
card_decal_data = [
    ('Bait Bucket', 'BaitBucket', 'blood2'),
    ('Great White', 'Shark', 'blood2'),
    ('The Smoke', 'Smoke', 'smoke'),
    ('Greater Smoke', 'Smoke_Improved', 'smoke'),
    ('Hungry Child', 'HungryChild', 'child'),
    ('Long Elk', 'LongElk', 'snelk')
]
for data in card_decal_data:
    cursor.execute('INSERT INTO card_decals (card_name, card_filename, decal_filename) VALUES (?, ?, ?)', data)

# Commit and disconnect
conn.commit()
conn.close()

print("Database 'inscryption.db' initialized.")
