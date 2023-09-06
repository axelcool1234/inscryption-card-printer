import sqlite3

# Connecting
conn = sqlite3.connect('inscryption.db')
cursor = conn.cursor()

# Dropping TABLEs
cursor.execute('DROP TABLE IF EXISTS flags;')
cursor.execute('DROP TABLE IF EXISTS staticons;')
cursor.execute('DROP TABLE IF EXISTS decals;')
cursor.execute('DROP TABLE IF EXISTS rarities;')
cursor.execute('DROP TABLE IF EXISTS notes;')
cursor.execute('DROP TABLE IF EXISTS temples;')
cursor.execute('DROP TABLE IF EXISTS sigils;')
cursor.execute('DROP TABLE IF EXISTS tribes;')
cursor.execute('DROP TABLE IF EXISTS cards;')
cursor.execute('DROP TABLE IF EXISTS card_tribes;')
cursor.execute('DROP TABLE IF EXISTS card_sigils;')
cursor.execute('DROP TABLE IF EXISTS card_flags;')
cursor.execute('DROP TABLE IF EXISTS card_decals;')
cursor.execute('DROP TABLE IF EXISTS card_before_decals;')
cursor.execute('DROP TABLE IF EXISTS death_cards;')
cursor.execute('DROP TABLE IF EXISTS card_staticons;')
cursor.execute('DROP TABLE IF EXISTS card_categories;')

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

cursor.execute('''CREATE TABLE rarities (
    name VARCHAR(45),
    filename TEXT PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE notes (
    id INT PRIMARY KEY,
    description TEXT DEFAULT '',
    mechanics TEXT DEFAULT '',
    gmNotes TEXT DEFAULT ''
);''')

cursor.execute('''CREATE TABLE temples (
    name VARCHAR(45),
    filename TEXT PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE sigils (
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY,
    power_level INT,
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
    blood_cost INTEGER DEFAULT 0,
    bone_cost INTEGER DEFAULT 0,
    energy_cost INTEGER DEFAULT 0,
    orange_mox_cost INTEGER DEFAULT 0,
    green_mox_cost INTEGER DEFAULT 0,
    blue_mox_cost INTEGER DEFAULT 0,
    rarity VARCHAR(10) NOT NULL,
    temple VARCHAR(10) NOT NULL,
    note_id INT,
    FOREIGN KEY (rarity) REFERENCES rarities (filename),
    FOREIGN KEY (temple) REFERENCES temples (filename)
);''')

cursor.execute('''CREATE TABLE death_cards(
    card_filename VARCHAR(45) PRIMARY KEY,
    ears VARCHAR(10),
    head VARCHAR(10),
    eyes VARCHAR(10),
    mouth VARCHAR(10),
    body VARCHAR(10),
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
    priority INT DEFAULT 1,
    PRIMARY KEY (card_filename, sigil_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (sigil_filename) REFERENCES sigils (filename)
);''')

cursor.execute('''CREATE TABLE card_flags (
    card_filename VARCHAR(45),  
    flag_filename INTEGER,          
    PRIMARY KEY (card_filename, flag_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (flag_filename) REFERENCES flags (name)
);''')

cursor.execute('''CREATE TABLE card_staticons (
    card_filename VARCHAR(45),  
    staticon_filename INTEGER,          
    PRIMARY KEY (card_filename, staticon_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (staticon_filename) REFERENCES staticons (name)
);''')


cursor.execute('''CREATE TABLE card_decals (
    card_filename VARCHAR(45),  
    decal_filename INTEGER,     
    PRIMARY KEY (card_filename, decal_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (decal_filename) REFERENCES flags (filename)
);''')

cursor.execute('''CREATE TABLE card_before_decals (
    card_filename VARCHAR(45),  
    before_decal_filename INTEGER,     
    PRIMARY KEY (card_filename, before_decal_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (before_decal_filename) REFERENCES flags (filename)
);''')

cursor.execute('''CREATE TABLE card_categories (
    card_filename VARCHAR(45) PRIMARY KEY,
    category VARCHAR(45)
);''')


# INSERT Statements
# Stat Icons
staticon_data = [
    ('ants',),
    ('sacrifices',),
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
    ('base_death_card',),
    ('no_portrait',),
    ('card_border',),
    ('card_bleed',)
]
for data in flag_data:
    cursor.execute('INSERT INTO flags (name) VALUES (?)', data)

# Decals
decal_data = [
    ('Blood', 'blood_1'),
    ('Blood', 'blood_2'),
    ('Blood', 'blood_3'),
    ('Blood', 'blood_4'),
    ('Paint', 'paint_1'),
    ('Paint', 'paint_2'),
    ('Paint', 'paint_3'),
    ('Long Elk', 'snelk'),
    ('Vertebrae', 'snelk_1'),
    ('Vertebrae', 'snelk_2'),
    ('Vertebrae', 'snelk_3'),
    ('Vertebrae', 'snelk_4'),
    ('Vertebrae', 'snelk_5'),
    ('Vertebrae', 'snelk_6'),
    ('Smoke', 'smoke'),
    ('Smoke', 'smoke_abilityhole'),
    ('Hungry Child', 'child'),
    ('Fungus', 'fungus'),
    ('Stitches', 'stitches'),
    ('Magnus', 'magnus'),
    ('Orange', 'orange'),
    ('Blue', 'blue'),
    ('Green', 'green'),
    ('Yellow Splatter', 'yellow_splatter'),
    ('Red Splatter', 'red_splatter'),
    ('Purple Splatter', 'purple_splatter'),
    ('Prism Splatter', 'prism_splatter'),
    ('Orange Splatter', 'orange_splatter'),
    ('Green Splatter', 'green_splatter'),
    ('Blue Splatter', 'blue_splatter'),
    ('Chain', 'chain'),
    ('Chara', 'chara'),
    ('Gaster', 'gaster'),
    ('Charged Luma Flies', 'chargedlumaflies'),
    ('Charged Luma Flies Attacking', 'chargedlumafliesattacking'),
    ('Gem Attack', 'gemattack'),
    ('Gem Cost', 'gemcost'),
    ('Gem Health', 'gemhealth'),
    ('Sand', 'sand'),
    ('Sand', 'sand_alt'),
    ('Shark Bite', 'shark_bite'),
    ('Spore', 'spore_0'),
    ('Spore', 'spore_1'),
    ('Spore', 'spore_2'),
    ('Undead', 'undead'),
    ('Worms', 'worms_0'),
    ('Worms', 'worms_1'),
    ('Worms', 'worms_2')
]
for data in decal_data:
    cursor.execute('INSERT INTO decals (name, filename) VALUES (?, ?)', data)

# Rarities
rarity_data = [
    ('Common', 'common'),
    ('Rare', 'rare'),
    ('Terrain', 'terrain'),
    ('Rare Terrain', 'rare_terrain'),
    ('Spell', 'spell')
]
for data in rarity_data:
    cursor.execute('INSERT INTO rarities (name, filename) VALUES (?, ?)', data)

# Notes
note_data = [

]
for data in note_data:
    cursor.execute('INSERT INTO notes (id, description, mechanics, gmNotes) VALUES (?, ?, ?, ?)', data)

# Temples
temple_data = [
    ('Nature', 'nature'),
    ('Undead', 'undead'),
    ('Tech', 'tech'),
    ('Wizard', 'wizard')
]
for data in temple_data:
    cursor.execute('INSERT INTO temples (name, filename) VALUES (?, ?)', data)

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
    ('Made of Stone', 'madeofstone', 2, None),
    ('Rabbit Hole', 'drawrabbits', 3, None),
    ('Bees Within', 'beesonhit', 3, None),
    ('Sprinter', 'strafe', 1, None),
    ('Touch of Death', 'deathtouch', 4, None),
    ('Fledgling', 'evolve', 2, None),
    ('Fledgling', 'evolve_1', 2,  None),
    ('Fledgling', 'evolve_2', 2,  None),
    ('Fledgling', 'evolve_3', 2, None),
    ('Dam Builder', 'createdams', 3, None),
    ('Hoarder', 'tutor', 4, None),
    ('Burrower', 'whackamole', 1, None),
    ('Fecundity', 'drawcopy', 3, None),
    ('Loose Tail', 'tailonhit', 2, None),
    ('Corpse Eater', 'corpseeater', 3, None),
    ('Bone King', 'quadruplebones', 2, None),
    ('Waterborne', 'submerge', 1, None),
    ('Unkillable', 'drawcopyondeath', 2, None),
    ('Sharp Quills', 'sharp', 2, None),
    ('Hefty', 'strafepush', 1, None),
    ('Rampager', 'strafeswap', 1, None),
    ('Brood Parasite', 'createegg', 4, None),
    ('Armored', 'deathshield', 4, None),
    ('Double Strike', 'doublestrike', 4, None),
    ('Morsel', 'morsel', 3, None),
    ('Blood Lust', 'gainattackonkill', 3, None),
    ('Scavenger', 'opponentbones', 2, None),
    ('Finical Hatchling', 'hydraegg', 4, None),
    ('Ant Spawner', 'drawant', 3, None),
    ('Guardian', 'guarddog', 1, None),
    ('Airborne', 'flying', 0, None),
    ('Many Lives', 'sacrificial', 4, None),
    ('Repulsive', 'preventattack', 4, None),
    ('Worthy Sacrifice', 'tripleblood', 2, None),
    ('Mighty Leap', 'reach', 1, None),
    ('Bifurcated Strike', 'splitstrike', 4, None),
    ('Trifurcated Strike', 'tristrike', 5, None),
    ('Frozen Away', 'icecube', 3, None),
    ('Sinkhole', 'sinkhole', 5, None),
    ('Bone Digger', 'bonedigger', 2, None),
    ('Trinket Bearer', 'randomconsumable', 5, None),
    ('Steel Trap', 'steeltrap', 5, None),
    ('Amorphous', 'randomability', 3, None),
    ('Tidal Lock', 'squirrelorbit', 5, None),
    ('Omni Strike', 'allstrike', 5, None),
    ('Leader', 'buffneighbours', 3, None),
    ('Brittle', 'brittle', -2, None),
    ('Skeleton Crew', 'skeletonstrafe', 3, None),
    ('Green Mox', 'gaingemgreen', 2, None),
    ('Orange Mox', 'gaingemorange', 2, None),
    ('Blue Mox', 'gaingemblue', 2, None),
    ('Gem Animator', 'buffgems', 3, None),
    ('Ruby Heart', 'droprubyondeath', 3, None),
    ('Mental Gemnastics', 'gemsdraw', 3, None),
    ('Gem Dependant', 'gemdependant', -3, None),
    ('Great Mox', 'gaingemtriple', 4, None),
    ('Handy', 'drawnewhand', 4, None),
    ('Squirrel Shedder', 'squirrelstrafe', 3, None),
    ('Attack Conduit', 'conduitbuffattack', 3, None),
    ('Spawn Conduit', 'conduitfactory', 3, None),
    ('Healing Conduit', 'conduitheal', 5, None),
    ('Null Conduit', 'conduitnull', 1, None),
    ('Battery Bearer', 'gainbattery', 2, None),
    ('Detonator', 'explodeondeath', 0, None),
    ('Sniper', 'sniper', 3, None),
    ('Nano Armor', 'deathshield_nano', 4, None),
    ('Overclocked', 'permadeath', -1, None),
    ('Bomb Latch', 'latchexplodeondeath', 2, None),
    ('Brittle Latch', 'latchbrittle', 3, None),
    ('Shield Latch', 'latchdeathshield', 1, None),
    ('Dead Byte', 'filesizedamage', 5, None),
    ('Hostage File', 'deletefile', 0, None),
    ('Transformer', 'transformer', 1, None),
    ('Sentry', 'sentry', 3, None),
    ('Gem Detonator', 1, 'explodegems', None),
    ('Gem Guardian', 'shieldgems', 2, None),
    ('Vessel Printer', 'drawvesselonhit', 2, None),
    ('Energy Conduit', 'conduitenergy', 2, None),
    ('Bomb Spewer', 'bombspawner', 4, None),
    ('Double Death', 'doubledeath', 3, None),
    ('Bone Dice', 'activatedrandompowerenergy', 3, None),
    ('Enlarge', 'activatedstatsup', 4, None),
    ('Swapper', 'swapstats', 0, None),
    ('Disentomb', 'activateddrawskeleton', 3, None),
    ('Energy Gun', 'activateddealdamage', 4, None),
    ('Bellist', 'createbells', 4, None),
    ('Annoying', 'buffenemy', -1, None),
    ('Gem Spawn Conduit', 'conduitspawngems', 3, None),
    ('Gift Bearer', 'drawrandomcardondeath', 3, None),
    ('Looter', 'loot', 4, None),
    ('True Scholar', 'activatedsacrificedrawcards', 3, None),
    ('Stimulate', 'activatedstatsupenergy', 4, None),
    ('Marrow Sucker', 'activatedheal', 1, None),
    ('Stinky', 'debuffenemy', 2, None),
    ('Buff When Powered', 'cellbuffself', 2, None),
    ('Gift When Powered', 'celldrawrandomcardondeath', 1, None),
    ('Trifurcated When Powered', 'celltristrike', 3, None),
    ('Bonehorn', 'activatedenergytobones', 4, None),
    ('Clinger', 'movebeside', 0, None),
    ('Kraken Waterborne', 'submergesquid', 2, None),
    ('Blood Guzzler', 'bloodguzzler', 0, None),
    ('Haunter', 'haunter', 0, None),
    ('Exploding Corpse', 'explodingcorpse', 0, None),
    ('Apparition', 'bloodymary', 0, None),
    ('Virtual Realist', 'virtualreality', 0, None),
    ('Head of Edaxio', 'edaxiohead', 0, None),
    ('Arms of Edaxio', 'edaxioarms', 0, None),
    ('Legs of Edaxio', 'edaxiolegs', 0, None),
    ('Torso of Edaxio', 'edaxiotorso', 0, None)
]
for data in sigil_data:
    cursor.execute('INSERT INTO sigils (name, filename, power_level, note_id) VALUES (?, ?, ?, ?)', data)

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
    ('Boulder', 'Boulder', 0, 5, 0, 'terrain', 'nature', None),
    ('Bullfrog', 'Bullfrog', 1, 2, 1, 'common', 'nature', None),
    ('Caged Wolf', 'CagedWolf', 0, 6, 2, 'terrain', 'nature', None),
    ('Cat', 'Cat', 0, 1, 1, 'common', 'nature', None),
    ('Undead Cat', 'UndeadCat', 3, 6, 1, 'common', 'nature', None),
    ('The Daus', 'Daus', 2, 2, 2, 'rare', 'nature', None),
    ('Elk', 'Elk', 2, 4, 2, 'common', 'nature', None),
    ('Elk Fawn', 'ElkFawn', 1, 1, 1, 'common', 'nature', None),
    ('Field Mice', 'FieldMice', 2, 2, 2, 'common', 'nature', None),
    ('Geck', 'Geck', 1, 1, None, 'rare', 'nature', None),
    ('Black Goat', 'Goat', 0, 1, 1, 'common', 'nature', None),
    ('Black Goat', 'Goat_Sexy', 0, 1, 1, 'common', 'nature', None),
    ('Grizzly', 'Grizzly', 4, 6, 3, 'common', 'nature', None),
    ('Child 13', 'JerseyDevil', 0, 1, 1, 'rare', 'nature', None),
    ('Child 13', 'JerseyDevil_Flying', 2, 1, 1, 'rare', 'nature', None),
    ('Kingfisher', 'Kingfisher', 1, 1, 1, 'common', 'nature', None),
    ('Magpie', 'Magpie', 1, 1, 2, 'common', 'nature', None),
    ('Mantis', 'Mantis', 1, 1, 1, 'common', 'nature', None),
    ('Mantis God', 'MantisGod', 1, 1, 1, 'rare', 'nature', None),
    ('Mole', 'Mole', 0, 4, 1, 'common', 'nature', None),
    ('Mole Man', 'MoleMan', 0, 6, 1, 'rare', 'nature', None),
    ('Mole Seaman', 'MoleSeaman', 1, 8, 1, 'rare', 'nature', None),
    ('Moose Buck', 'Moose', 3, 7, 3, 'common', 'nature', None),
    ('Strange Larva', 'Mothman_1', 0, 3, 1, 'rare', 'nature', None),
    ('Strange Pupa', 'Mothman_2', 0, 3, 1, 'rare', 'nature', None),
    ('Mothman', 'Mothman_3', 7, 3, 1, 'rare', 'nature', None),
    ('Pack Mule', 'Mule', 0, 5, None, 'common', 'nature', None),
    ('River Otter', 'Otter', 1, 1, 1, 'common', 'nature', None),
    ('Ouroboros', 'Ouroboros', 1, 1, 2, 'rare', 'nature', None),
    ('Pack Rat', 'PackRat', 2, 2, 2, 'rare', 'nature', None),
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
    ('Urayuli', 'Urayuli', 7, 7, 4, 'rare', 'nature', None),
    ('Vertebrae', 'Vertebrae', 0, 1, 0, 'common', 'nature', None),
    ('Warren', 'Warren', 0, 2, 1, 'common', 'nature', None),
    ('Wolf', 'Wolf', 3, 2, 2, 'common', 'nature', None),
    ('Wolf Cub', 'WolfCub', 1, 1, 1, 'common', 'nature', None),
    ('Bait Bucket', 'BaitBucket', 0, 1, 0, 'terrain', 'nature', None),
    ('Broken Egg', 'BrokenEgg', 0, 1, 0, 'terrain', 'nature', None),
    ('Dam', 'Dam', 0, 2, 0, 'terrain', 'nature', None),
    ('Chime', 'DausBell', 0, 1, 0, 'terrain', 'nature', None),
    ('Gold Nugget', 'GoldNugget', 0, 2, 0, 'terrain', 'nature', None),
    ('Golden Pelt', 'Pelt_Golden', 0, 3, 0, 'terrain', 'nature', None),
    ('Rabbit Pelt', 'Pelt_Hare', 0, 1, 0, 'terrain', 'nature', None),
    ('Wolf Pelt', 'Pelt_Wolf', 0, 2, 0, 'terrain', 'nature', None),
    ('Ring Worm', 'RingWorm', 0, 1, 1, 'common', 'nature', None),
    ('Stoat', 'Stoat', 1, 2, 1, 'common', 'nature', None),
    ('The Smoke', 'Smoke', 0, 1, 0, 'common', 'nature', None),
    ('Greater Smoke', 'Smoke_Improved', 1, 3, 0, 'common', 'nature', None),
    ('Starvation', 'StarvingMan', None, None, 0, 'common', 'nature', None),
    ('Starvation', 'StarvingMan_Flight', None, None, 0, 'common', 'nature', None),
    ('Leaping Trap', 'Trap', 0, 1, 0, 'terrain', 'nature', None),
    ('Strange Frog', 'TrapFrog', 1, 2, 1, 'terrain', 'nature', None),
    ('Frozen Opossum', 'Frozen_Opossum', 0, 5, 0, 'terrain', 'nature', None),
    ('Snowy Fir', 'Tree_SnowCovered', 0, 4, 0, 'terrain', 'nature', None),
    ('Grand Fir', 'Tree', 0, 3, 0, 'terrain', 'nature', None),
    ('Hungry Child', 'Child', 0, 0, 0, 'common', 'nature', None),
    ('Stump', 'Stump', 0, 3, 0, 'terrain', 'nature', None),
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
    ('Pelt Lice', 'Lice', 1, 1, 4, 'rare', 'nature', None),
    ('Hodag', 'Hodag', 1, 5, 2, 'rare', 'nature', None),
    ('Great Kraken', 'Kraken', 1, 1, 1, 'rare', 'nature', None),
    ('Louis', 'Louis', 1, 1, 1, 'common', 'nature', None),
    ('Kaycee', 'Kaycee', 1, 2, 1, 'common', 'nature', None)
]
for data in blood_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, blood_cost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# Bone Cards
bone_card_data = [
    ('Alpha', 'Alpha', 1, 2, 4, 'common', 'nature', None),
    ('Amoeba', 'Amoeba', 1, 2, 2, 'rare', 'nature', None),
    ('Bat', 'Bat', 2, 1, 4, 'common', 'nature', None),
    ('Cockroach', 'Cockroach', 1, 1, 4, 'common', 'nature', None),
    ('Coyote', 'Coyote', 2, 1, 4, 'common', 'nature', None),
    ('Corpse Maggots', 'Maggots', 1, 2, 5, 'common', 'nature', None),
    ('Opossum', 'Opossum', 1, 1, 2, 'common', 'nature', None),
    ('Rattler', 'Rattler', 3, 1, 6, 'common', 'nature', None),
    ('Long Elk', 'LongElk', 1, 2, 4, 'rare', 'nature', None),
    ('Stinkbug', 'Stinkbug_Talking', 1, 2, 2, 'common', 'nature', None),
    ('Turkey Vulture', 'Vulture', 3, 3, 8, 'common', 'nature', None),
    ('Mealworm', 'MealWorm', 0, 2, 2, 'common', 'nature', None),
    ('Wolverine', 'Wolverine', 1, 3, 5, 'common', 'nature', None),
    ('Curious Egg', 'HydraEgg', 0, 1, 1, 'rare', 'nature', None),
    ('Hydra', 'Hydra', 1, 5, 1, 'rare', 'nature', None),
    ('Reginald', 'Reginald', 1, 3, 3, 'common', 'nature', None),
    ('Kaminski', 'Kaminski', 0, 1, 1, 'common', 'nature', None)
]
for data in bone_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, bone_cost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# Energy Cards
energy_card_data = [

]
for data in energy_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, energy_cost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# (Orange, Green, Blue) Mox Cards
mox_card_data = [

]
for data in mox_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, orange_mox_cost, green_mox_cost, blue_mox_cost, rarity, temple, note_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', data)

# Multi-Cost Cards
# Will implement when needed


# Card Categories
card_category_data = [
    # Base game cards
    ('Adder', 'base'),
    ('Amalgam', 'base'),
    ('Ant', 'base'),
    ('AntQueen', 'base'),
    ('Beaver', 'base'),
    ('Bee', 'base'),
    ('Beehive', 'base'),
    ('Bloodhound', 'base'),
    ('Boulder', 'base'),
    ('Bullfrog', 'base'),
    ('CagedWolf', 'base'),
    ('Cat', 'base'),
    ('UndeadCat', 'base'),
    ('Daus', 'base'),
    ('Elk', 'base'),
    ('ElkFawn', 'base'),
    ('FieldMice', 'base'),
    ('Geck', 'base'),
    ('Goat', 'base'),
    ('Goat_Sexy', 'base'),
    ('Grizzly', 'base'),
    ('JerseyDevil', 'base'),
    ('JerseyDevil_Flying', 'base'),
    ('Kingfisher', 'base'),
    ('Magpie', 'base'),
    ('Mantis', 'base'),
    ('MantisGod', 'base'),
    ('Mole', 'base'),
    ('MoleMan', 'base'),
    ('MoleSeaman', 'base'),
    ('Moose', 'base'),
    ('Mothman_1', 'base'),
    ('Mothman_2', 'base'),
    ('Mothman_3', 'base'),
    ('Mule', 'base'),
    ('Otter', 'base'),
    ('Ouroboros', 'base'),
    ('PackRat', 'base'),
    ('Porcupine', 'base'),
    ('Pronghorn', 'base'),
    ('Rabbit', 'base'),
    ('RatKing', 'base'),
    ('Raven', 'base'),
    ('RavenEgg', 'base'),
    ('Shark', 'base'),
    ('Shark_Bloodless', 'base'),
    ('Skink', 'base'),
    ('Skunk', 'base'),
    ('Turtle', 'base'),
    ('Sparrow', 'base'),
    ('SquidBell', 'base'),
    ('SquidCards', 'base'),
    ('SquidMirror', 'base'),
    ('Squirrel', 'base'),
    ('Stoat_Talking', 'base'),
    ('Wolf_Talking', 'base'),
    ('Skink_Tail', 'base'),
    ('Bird_Tail', 'base'),
    ('Canine_Tail', 'base'),
    ('Insect_Tail', 'base'),
    ('Urayuli', 'base'),
    ('Vertebrae', 'base'),
    ('Warren', 'base'),
    ('Wolf', 'base'),
    ('WolfCub', 'base'),
    ('BaitBucket', 'base'),
    ('BrokenEgg', 'base'),
    ('Dam', 'base'),
    ('DausBell', 'base'),
    ('GoldNugget', 'base'),
    ('Pelt_Golden', 'base'),
    ('Pelt_Hare', 'base'),
    ('Pelt_Wolf', 'base'),
    ('RingWorm', 'base'),
    ('Stoat', 'base'),
    ('Smoke', 'base'),
    ('Smoke_Improved', 'base'),
    ('StarvingMan', 'base'),
    ('StarvingMan_Flight', 'base'),
    ('Trap', 'base'),
    ('TrapFrog', 'base'),
    ('Frozen_Opossum', 'base'),
    ('Tree_SnowCovered', 'base'),
    ('Tree', 'base'),
    ('Child', 'base'),
    ('Stump', 'base'),
    ('AquaSquirrel', 'base'),
    ('SkeletonPirate', 'base'),
    ('SkeletonParrot', 'base'),
    ('Bull', 'base'),
    ('Cuckoo', 'base'),
    ('Ijiraq', 'base'),
    ('AntFlying', 'base'),
    ('MudTurtle_Shelled', 'base'),
    ('MudTurtle', 'base'),
    ('DireWolfCub', 'base'),
    ('DireWolf', 'base'),
    ('Raccoon', 'base'),
    ('Lammergeier', 'base'),
    ('RedHart', 'base'),
    ('Tadpole', 'base'),
    ('Lice', 'base'),
    ('Hodag', 'base'),
    ('Kraken', 'base'),
    ('Louis', 'base'),
    ('Kaycee', 'base'),
    ('Alpha', 'base'),
    ('Amoeba', 'base'),
    ('Bat', 'base'),
    ('Cockroach', 'base'),
    ('Coyote', 'base'),
    ('Maggots', 'base'),
    ('Opossum', 'base'),
    ('Rattler', 'base'),
    ('LongElk', 'base'),
    ('Stinkbug_Talking', 'base'),
    ('Vulture', 'base'),
    ('MealWorm', 'base'),
    ('Wolverine', 'base'),
    ('HydraEgg', 'base'),
    ('Hydra', 'base'),
    ('Reginald', 'base'),
    ('Kaminski', 'base')

    # Custom
]
for data in card_category_data:
    cursor.execute('INSERT INTO card_categories (card_filename, category) VALUES (?, ?)', data)


#Death Cards
death_card_data = [
    ('Reginald', None, 'settlerman', 3, 6, 'base', 'False' ),
    ('Louis', None, 'chief', 1, 3, 'base', 'False' ),
    ('Kaminski', None, 'settlerwoman', 2, 4, 'base', 'False' ),
    ('Kaycee', None, 'wildling', 5, 2, 'base', 'False')
]
for data in death_card_data:
    cursor.execute('INSERT INTO death_cards (card_filename, ears, head, eyes, mouth, body, lost_eye) VALUES (?, ?, ?, ?, ?, ?, ?)', data)

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
    ('Wolf_Talking', 'canine'),
    ('Vertebrae', 'hooved'),
    ('Wolf', 'canine'),
    ('WolfCub', 'canine'),
    ('RingWorm', 'insect'),
    ('Bull', 'hooved'),
    ('Cuckoo', 'bird'),
    ('AntFlying', 'insect'),
    ('MudTurtle_Shelled', 'reptile'),
    ('MudTurtle', 'reptile'),
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

# Card Sigils (Single)
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
    ('Elk', 'strafe'),
    ('FieldMice', 'drawcopy'),
    ('Goat', 'tripleblood'),
    ('Goat_Sexy', 'tripleblood'),
    ('JerseyDevil', 'sacrificial'),
    ('Maggots', 'corpseeater'),
    ('Mantis', 'splitstrike'),
    ('MantisGod', 'tristrike'),
    ('Mole', 'whackamole'),
    ('Moose', 'strafepush'),
    ('Mothman_1', 'evolve_1'),
    ('Mothman_2', 'evolve_1'),
    ('Mothman_3', 'flying'),
    ('Mule', 'strafe'),
    ('Otter', 'submerge'),
    ('Ouroboros', 'drawcopyondeath'),
    ('PackRat', 'randomconsumable'),
    ('Porcupine', 'sharp'),
    ('RatKing', 'quadruplebones'),
    ('Raven', 'flying'),
    ('RavenEgg', 'evolve_1'),
    ('Shark', 'submerge'),
    ('Shark_Bloodless', 'submerge'),
    ('Skink', 'tailonhit'),
    ('Skunk', 'debuffenemy'),
    ('Sparrow', 'flying'),
    ('Stinkbug_Talking', 'debuffenemy'),
    ('Vulture', 'flying'),
    ('Warren', 'drawrabbits'),
    ('WolfCub', 'evolve_1'),
    ('Smoke', 'quadruplebones'),
    ('Smoke_Improved', 'quadruplebones'),
    ('StarvingMan', 'preventattack'),
    ('TrapFrog', 'reach'),
    ('Frozen_Opossum', 'icecube'),
    ('Tree_SnowCovered', 'reach'),
    ('Tree', 'reach'),
    ('AquaSquirrel', 'submerge'),
    ('SkeletonPirate', 'brittle'),
    ('Bull', 'strafeswap'),
    ('Ijiraq', 'preventattack'),
    ('AntFlying', 'flying'),
    ('MudTurtle_Shelled', 'deathshield'),
    ('DireWolf', 'doublestrike'),
    ('MealWorm', 'morsel'),
    ('Wolverine', 'gainattackonkill'),
    ('Raccoon', 'opponentbones'),
    ('Lammergeier', 'flying'),
    ('RedHart', 'strafe'),
    ('Lice', 'doublestrike'),
    ('Hodag', 'gainattackonkill'),
    ('Kraken', 'submergesquid'),
    ('HydraEgg', 'hydraegg'),
    ('Reginald', 'deathtouch'),
]
for data in card_sigil_data:
    cursor.execute('INSERT INTO card_sigils (card_filename, sigil_filename) VALUES (?, ?)', data)

# Card Sigils (Multi)
card_sigil_data = [
    ('ElkFawn', 'strafe', 1),
    ('ElkFawn', 'evolve_1', 2),
    ('JerseyDevil_Flying', 'sacrificial', 1),
    ('JerseyDevil_Flying', 'flying', 2),
    ('DireWolfCub', 'bonedigger', 1),
    ('DireWolfCub', 'evolve_1', 2),
    ('Kingfisher', 'flying', 1),
    ('Kingfisher', 'submerge', 2),
    ('Magpie', 'flying', 1),
    ('Magpie', 'tutor', 2),
    ('MoleMan', 'whackamole', 1),
    ('MoleMan', 'reach', 2),
    ('MoleSeaman', 'whackamole', 1),
    ('MoleSeaman', 'reach', 2),
    ('Pronghorn', 'strafe', 1),
    ('Pronghorn', 'splitstrike', 2),
    ('LongElk', 'strafe', 1),
    ('LongElk', 'deathtouch', 2),
    ('StarvingMan_Flight', 'preventattack', 1),
    ('StarvingMan_Flight', 'flying', 2),
    ('Trap', 'reach', 1),
    ('Trap', 'steeltrap', 2),
    ('SkeletonParrot', 'flying', 1),
    ('SkeletonParrot', 'brittle', 2),
    ('Cuckoo', 'flying', 1),
    ('Cuckoo', 'createegg', 2),
    ('Tadpole', 'submerge', 1),
    ('Tadpole', 'evolve_1', 2),
    ('Hydra', 'splitstrike', 1),
    ('Hydra', 'tristrike', 2),
    ('Louis', 'strafe', 1),
    ('Louis', 'submerge', 2),
    ('Kaminski', 'guarddog', 1),
    ('Kaminski', 'sharp', 2),
    ('Kaycee', 'splitstrike', 1),
    ('Kaycee', 'sharp', 2)
]
for data in card_sigil_data:
    cursor.execute('INSERT INTO card_sigils (card_filename, sigil_filename, priority) VALUES (?, ?, ?)', data)

# Card Flags
card_flag_data = [
    ('SquidBell', 'squid'),
    ('SquidCards', 'squid'),
    ('SquidMirror', 'squid'),
    ('GoldNugget', 'golden'),
    ('GoldNugget', 'emission'),
    ('Pelt_Golden', 'golden'),
    ('Pelt_Golden', 'emission'),
    ('Smoke_Improved', 'emission'),
    ('StarvingMan', 'hide_power_and_health'),
    ('StarvingMan_Flight', 'hide_power_and_health'),
    ('Reginald', 'base_death_card'),
    ('Louis', 'base_death_card'),
    ('Kaminski', 'base_death_card'),
    ('Kaycee', 'base_death_card'),
    ('Vertebrae', 'no_portrait'),
    ('LongElk', 'no_portrait'),
    ('Child', 'no_portrait'),
    ('Frozen_Opossum', 'no_terrain_layout'),
    ('TrapFrog', 'no_terrain_layout')
]
for data in card_flag_data:
    cursor.execute('INSERT INTO card_flags (card_filename, flag_filename) VALUES (?, ?)', data)

# Card Staticons
card_staticon_data = [
    ('Ant', 'ants'),
    ('AntQueen', 'ants'),
    ('SquidBell', 'bell'),
    ('SquidCards', 'cardsinhand'),
    ('SquidMirror', 'mirror'),
    ('AntFlying', 'ants'),
    ('Lammergeier', 'bones'),
    ('RedHart', 'sacrifices'),
]
for data in card_staticon_data:
    cursor.execute('INSERT INTO card_staticons (card_filename, staticon_filename) VALUES (?, ?)', data)

# Card Decals
card_decal_data = [
    ('BaitBucket', 'blood_2'),
    ('Shark', 'blood_2'),
    ('Smoke', 'smoke'),
    ('Smoke_Improved', 'smoke'),
    ('Child', 'child'),
    ('LongElk', 'snelk'),
    ('Vertebrae', 'snelk_4'),
]
for data in card_decal_data:
    cursor.execute('INSERT INTO card_decals (card_filename, decal_filename) VALUES (?, ?)', data)

# Card Decals (Before Portrait)
card_before_decal_data = [

]
for data in card_decal_data:
    cursor.execute('INSERT INTO card_before_decals (card_filename, before_decal_filename) VALUES (?, ?)', data)

# Commit and disconnect
conn.commit()
conn.close()

print("Database 'inscryption.db' initialized.")
