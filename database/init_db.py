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
cursor.execute('DROP TABLE IF EXISTS boons;')
cursor.execute('DROP TABLE IF EXISTS items;')
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
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY
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
    filename VARCHAR(45),
    type VARCHAR(45),
    description TEXT DEFAULT '',
    mechanics TEXT DEFAULT '',
    gmNotes TEXT DEFAULT '',
    PRIMARY KEY (filename, type)
);''')

cursor.execute('''CREATE TABLE boons (
    name VARCHAR(45),
    filename TEXT PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE items (
    name VARCHAR(45),
    filename TEXT PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE temples (
    name VARCHAR(45),
    filename TEXT PRIMARY KEY
);''')

cursor.execute('''CREATE TABLE sigils (
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY,
    power_level INT
);''')

cursor.execute(''' CREATE TABLE tribes (
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY,
    priority INT
);''')

cursor.execute('''CREATE TABLE cards (
    name VARCHAR(45),
    filename VARCHAR(45) PRIMARY KEY,
    power INTEGER,
    health INTEGER,
    cost VARCHAR(45),
    rarity VARCHAR(10) NOT NULL,
    temple VARCHAR(10) NOT NULL,
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
    FOREIGN KEY (decal_filename) REFERENCES decals (filename)
);''')

cursor.execute('''CREATE TABLE card_before_decals (
    card_filename VARCHAR(45),  
    before_decal_filename INTEGER,     
    PRIMARY KEY (card_filename, before_decal_filename),
    FOREIGN KEY (card_filename) REFERENCES cards (filename),
    FOREIGN KEY (before_decal_filename) REFERENCES decals (filename)
);''')

cursor.execute('''CREATE TABLE card_categories (
    card_filename VARCHAR(45) PRIMARY KEY,
    category VARCHAR(45)
);''')


# INSERT Statements
# Stat Icons
staticon_data = [
    ('Ants', 'ants',),
    ('Sacrifices', 'sacrifices',),
    ('Bell', 'bell',),
    ('Cards In Hand', 'cardsinhand',),
    ('Mirror', 'mirror',),
    ('Bones', 'bones',),
    ('Green Gems', 'greengems',)
]
for data in staticon_data:
    cursor.execute('INSERT INTO staticons (name, filename) VALUES (?, ?)', data)

# Boons
boon_data = [
    ("Boon of Goat's Blood", 'startinggoat'),
    ("Boon of the Ambidextrous", 'doubledraw'),
    ("Boon of the Bone Lord", 'startingbones'),
    ("Boon of the Forest", 'startingtrees'),
    ("Boon of the Magpie's Eye", 'tutordraw'),
    ("Minor Boon of the Bone Lord", 'singlestartingbone')
]
for data in boon_data:
    cursor.execute('INSERT INTO boons (name, filename) VALUES (?, ?)', data)

# Items
item_data = [
    ("Black Goat Bottle", 'goatbottle'),
    ("Boulder in a Bottle", 'terrainbottle'),
    ("Failure", 'goobottle'),
    ("Fish Hook", 'fishhook'),
    ("Frozen Opossum Bottle", 'frozenopossumbottle'),
    ("Harpie's Birdleg Fan", 'birdlegfan'),
    ("Hoggy Bank", 'piggybank'),
    ("Hourglass", 'hourglass'),
    ("Magickal Bleach", 'bleachpot'),
    ("Magpie's Glass", 'magnifyingglass'),
    ("Pliers", 'pliers'),
    ("Scissors", 'scissors'),
    ("Skinning Knife", 'trapperknife'),
    ("Special Dagger", 'specialdagger'),
    ("Squirrel in a Bottle", 'squirrelbottle'),
    ("Wiseclock", 'pocketwatch'),

    # Act 3
    # ('Extra Battery', ),
    # ("Mrs. Bomb's Remote", ),
    # ('Nano Armor Generator', ),

    # Custom (axel)
    # ('Prism Mox in a Bottle', ),
]
for data in item_data:
    cursor.execute('INSERT INTO items (name, filename) VALUES (?, ?)', data)

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
    ('Avian', 'bird', 1),
    ('Canine', 'canine', 2),
    ('Hooved', 'hooved', 3),
    ('Reptilian', 'reptile', 4),
    ('Insectoid', 'insect', 5)
]
for data in tribe_data:
    cursor.execute('INSERT INTO tribes (name, filename, priority) VALUES (?, ?, ?)', data)

# Sigils
sigil_data = [
    ('Made of Stone', 'madeofstone', 2),
    ('Rabbit Hole', 'drawrabbits', 3),
    ('Bees Within', 'beesonhit', 3),
    ('Sprinter', 'strafe', 1),
    ('Touch of Death', 'deathtouch', 4),
    ('Fledgling', 'evolve', 2),
    ('Fledgling', 'evolve_1', 2),
    ('Fledgling', 'evolve_2', 2),
    ('Fledgling', 'evolve_3', 2),
    ('Dam Builder', 'createdams', 3),
    ('Hoarder', 'tutor', 4),
    ('Burrower', 'whackamole', 1),
    ('Fecundity', 'drawcopy', 3),
    ('Loose Tail', 'tailonhit', 2),
    ('Corpse Eater', 'corpseeater', 3),
    ('Bone King', 'quadruplebones', 2),
    ('Waterborne', 'submerge', 1),
    ('Unkillable', 'drawcopyondeath', 2),
    ('Sharp Quills', 'sharp', 2),
    ('Hefty', 'strafepush', 1),
    ('Rampager', 'strafeswap', 1),
    ('Brood Parasite', 'createegg', 4),
    ('Armored', 'deathshield', 4),
    ('Double Strike', 'doublestrike', 4),
    ('Morsel', 'morsel', 3),
    ('Blood Lust', 'gainattackonkill', 3),
    ('Scavenger', 'opponentbones', 2),
    ('Finical Hatchling', 'hydraegg', 4),
    ('Ant Spawner', 'drawant', 3),
    ('Guardian', 'guarddog', 1),
    ('Airborne', 'flying', 0),
    ('Many Lives', 'sacrificial', 4),
    ('Repulsive', 'preventattack', 4),
    ('Worthy Sacrifice', 'tripleblood', 2),
    ('Mighty Leap', 'reach', 1),
    ('Bifurcated Strike', 'splitstrike', 4),
    ('Trifurcated Strike', 'tristrike', 5),
    ('Frozen Away', 'icecube', 3),
    ('Sinkhole', 'sinkhole', 5),
    ('Bone Digger', 'bonedigger', 2),
    ('Trinket Bearer', 'randomconsumable', 5),
    ('Steel Trap', 'steeltrap', 5),
    ('Amorphous', 'randomability', 3),
    ('Tidal Lock', 'squirrelorbit', 5),
    ('Omni Strike', 'allstrike', 5),
    ('Leader', 'buffneighbours', 3),
    ('Brittle', 'brittle', -2),
    ('Skeleton Crew', 'skeletonstrafe', 3),
    ('Green Mox', 'greenmox', 2),
    ('Orange Mox', 'orangemox', 2),
    ('Blue Mox', 'bluemox', 2),
    ('Gem Animator', 'buffgems', 3),
    ('Ruby Heart', 'droprubyondeath', 3),
    ('Mental Gemnastics', 'gemsdraw', 3),
    ('Gem Dependant', 'gemdependant', -3),
    ('Great Mox', 'gaingemtriple', 4),
    ('Handy', 'drawnewhand', 4),
    ('Squirrel Shedder', 'squirrelstrafe', 3),
    ('Attack Conduit', 'conduitbuffattack', 3),
    ('Spawn Conduit', 'conduitfactory', 3),
    ('Healing Conduit', 'conduitheal', 5),
    ('Null Conduit', 'conduitnull', 1),
    ('Battery Bearer', 'gainbattery', 2),
    ('Detonator', 'explodeondeath', 0),
    ('Sniper', 'sniper', 3),
    ('Nano Armor', 'deathshield_nano', 4),
    ('Overclocked', 'permadeath', -1),
    ('Bomb Latch', 'latchexplodeondeath', 2),
    ('Brittle Latch', 'latchbrittle', 3),
    ('Shield Latch', 'latchdeathshield', 1),
    ('Dead Byte', 'filesizedamage', 5),
    ('Hostage File', 'deletefile', 0),
    ('Transformer', 'transformer', 1),
    ('Sentry', 'sentry', 3),
    ('Gem Detonator', 'explodegems', 1),
    ('Gem Guardian', 'shieldgems', 2),
    ('Vessel Printer', 'drawvesselonhit', 2),
    ('Energy Conduit', 'conduitenergy', 2),
    ('Bomb Spewer', 'bombspawner', 4),
    ('Double Death', 'doubledeath', 3),
    ('Power Dice', 'activatedrandompowerenergy', 3),
    ('Enlarge', 'activatedstatsup', 4),
    ('Swapper', 'swapstats', 0),
    ('Disentomb', 'activateddrawskeleton', 3),
    ('Energy Gun', 'activateddealdamage', 4),
    ('Bellist', 'createbells', 4),
    ('Annoying', 'buffenemy', -1),
    ('Gem Spawn Conduit', 'conduitspawngems', 3),
    ('Gift Bearer', 'drawrandomcardondeath', 3),
    ('Looter', 'loot', 4),
    ('True Scholar', 'activatedsacrificedrawcards', 3),
    ('Stimulate', 'activatedstatsupenergy', 4),
    #('Marrow Sucker', 'activatedheal', 1),
    ('Stinky', 'debuffenemy', 2),
    ('Buff When Powered', 'cellbuffself', 2),
    ('Gift When Powered', 'celldrawrandomcardondeath', 1),
    ('Trifurcated When Powered', 'celltristrike', 3),
    ('Bonehorn', 'activatedenergytobones', 4),
    ('Clinger', 'movebeside', 0),
    ('Waterborne', 'submergesquid', 2),
    ('Blood Guzzler', 'bloodguzzler', 0),
    ('Haunter', 'haunter', 0),
    ('Exploding Corpse', 'explodingcorpse', 0),
    ('Apparition', 'bloodymary', 0),
    ('Virtual Realist', 'virtualreality', 0),
    ('Head of Edaxio', 'edaxiohead', 0),
    ('Arms of Edaxio', 'edaxioarms', 0),
    ('Legs of Edaxio', 'edaxiolegs', 0),
    ('Torso of Edaxio', 'edaxiotorso', 0)
]
for data in sigil_data:
    cursor.execute('INSERT INTO sigils (name, filename, power_level) VALUES (?, ?, ?)', data)

# Blood Cards
blood_card_data = [
    # Blood Cards (Base Game)
    ('Adder', 'Adder', 1, 1, 'blood_2', 'common', 'nature'),
    ('Amalgam', 'Amalgam', 3, 3, 'blood_2', 'rare', 'nature'),
    ('Worker Ant', 'Ant', None, 2, 'blood_1', 'common', 'nature'),
    ('Ant Queen', 'AntQueen', None, 3, 'blood_2', 'common', 'nature'),
    ('Beaver', 'Beaver', 1, 4, 'blood_2', 'common', 'nature'),
    ('Bee', 'Bee', 1, 1, None, 'common', 'nature'),
    ('Beehive', 'Beehive', 0, 2, 'blood_1', 'common', 'nature'),
    ('Bloodhound', 'Bloodhound', 2, 3, 'blood_2', 'common', 'nature'),
    ('Boulder', 'Boulder', 0, 5, None, 'terrain', 'nature'),
    ('Bullfrog', 'Bullfrog', 1, 2, 'blood_1', 'common', 'nature'),
    ('Caged Wolf', 'CagedWolf', 0, 6, 'blood_2', 'terrain', 'nature'),
    ('Cat', 'Cat', 0, 1, 'blood_1', 'common', 'nature'),
    ('Undead Cat', 'UndeadCat', 3, 6, 'blood_1', 'common', 'nature'),
    ('The Daus', 'Daus', 2, 2, 'blood_2', 'rare', 'nature'),
    ('Elk', 'Elk', 2, 4, 'blood_2', 'common', 'nature'),
    ('Elk Fawn', 'ElkFawn', 1, 1, 'blood_1', 'common', 'nature'),
    ('Field Mice', 'FieldMice', 2, 2, 'blood_2', 'common', 'nature'),
    ('Geck', 'Geck', 1, 1, None, 'rare', 'nature'),
    ('Black Goat', 'Goat', 0, 1, 'blood_1', 'common', 'nature'),
    ('Black Goat', 'Goat_Sexy', 0, 1, 'blood_1', 'common', 'nature'),
    ('Grizzly', 'Grizzly', 4, 6, 'blood_3', 'common', 'nature'),
    ('Child 13', 'JerseyDevil', 0, 1, 'blood_1', 'rare', 'nature'),
    ('Child 13', 'JerseyDevil_Flying', 2, 1, 'blood_1', 'rare', 'nature'),
    ('Kingfisher', 'Kingfisher', 1, 1, 'blood_1', 'common', 'nature'),
    ('Magpie', 'Magpie', 1, 1, 'blood_2', 'common', 'nature'),
    ('Mantis', 'Mantis', 1, 1, 'blood_1', 'common', 'nature'),
    ('Mantis God', 'MantisGod', 1, 1, 'blood_1', 'rare', 'nature'),
    ('Mole', 'Mole', 0, 4, 'blood_1', 'common', 'nature'),
    ('Mole Man', 'MoleMan', 0, 6, 'blood_1', 'rare', 'nature'),
    ('Mole Seaman', 'MoleSeaman', 1, 8, 'blood_1', 'rare', 'nature'),
    ('Moose Buck', 'Moose', 3, 7, 'blood_3', 'common', 'nature'),
    ('Strange Larva', 'Mothman_1', 0, 3, 'blood_1', 'rare', 'nature'),
    ('Strange Pupa', 'Mothman_2', 0, 3, 'blood_1', 'rare', 'nature'),
    ('Mothman', 'Mothman_3', 7, 3, 'blood_1', 'rare', 'nature'),
    ('Pack Mule', 'Mule', 0, 5, None, 'common', 'nature'),
    ('River Otter', 'Otter', 1, 1, 'blood_1', 'common', 'nature'),
    ('Ouroboros', 'Ouroboros', 1, 1, 'blood_2', 'rare', 'nature'),
    ('Pack Rat', 'PackRat', 2, 2, 'blood_2', 'rare', 'nature'),
    ('Porcupine', 'Porcupine', 1, 2, 'blood_1', 'common', 'nature'),
    ('Pronghorn', 'Pronghorn', 1, 3, 'blood_2', 'common', 'nature'),
    ('Rabbit', 'Rabbit', 0, 1, None, 'common', 'nature'),
    ('Rat King', 'RatKing', 2, 1, 'blood_2', 'common', 'nature'),
    ('Raven', 'Raven', 2, 3, 'blood_2', 'common', 'nature'),
    ('Raven Egg', 'RavenEgg', 0, 2, 'blood_1', 'common', 'nature'),
    ('Great White', 'Shark', 4, 2, 'blood_3', 'common', 'nature'),
    ('Great White', 'Shark_Bloodless', 4, 2, 'blood_3', 'common', 'nature'),
    ('Skink', 'Skink', 1, 2, 'blood_1', 'common', 'nature'),
    ('Skunk', 'Skunk', 0, 3, 'blood_1', 'common', 'nature'),
    ('River Snapper', 'Turtle', 1, 6, 'blood_2', 'common', 'nature'),
    ('Sparrow', 'Sparrow', 1, 2, 'blood_1', 'common', 'nature'),
    ('squid_bell', 'SquidBell', None, 3, 'blood_2', 'common', 'nature'),
    ('squid_cards', 'SquidCards', None, 1, 'blood_1', 'common', 'nature'),
    ('squid_mirror', 'SquidMirror', None, 3, 'blood_1', 'common', 'nature'),
    ('Squirrel', 'Squirrel', 0, 1, None, 'common', 'nature'),
    ('Stoat', 'Stoat_Talking', 1, 3, 'blood_1', 'common', 'nature'),
    ('Stunted Wolf', 'Wolf_Talking', 2, 2, 'blood_1', 'common', 'nature'),
    ('Wriggling Tail', 'Skink_Tail', 0, 2, None, 'common', 'nature'),
    ('Tail Feathers', 'Bird_Tail', 0, 2, None, 'common', 'nature'),
    ('Furry Tail', 'Canine_Tail', 0, 2, None, 'common', 'nature'),
    ('Wriggling Leg', 'Insect_Tail', 0, 2, None, 'common', 'nature'),
    ('Urayuli', 'Urayuli', 7, 7, 'blood_4', 'rare', 'nature'),
    ('Vertebrae', 'Vertebrae', 0, 1, None, 'common', 'nature'),
    ('Warren', 'Warren', 0, 2, 'blood_1', 'common', 'nature'),
    ('Wolf', 'Wolf', 3, 2, 'blood_2', 'common', 'nature'),
    ('Wolf Cub', 'WolfCub', 1, 1, 'blood_1', 'common', 'nature'),
    ('Bait Bucket', 'BaitBucket', 0, 1, None, 'terrain', 'nature'),
    ('Broken Egg', 'BrokenEgg', 0, 1, None, 'terrain', 'nature'),
    ('Dam', 'Dam', 0, 2, None, 'terrain', 'nature'),
    ('Chime', 'DausBell', 0, 1, None, 'terrain', 'nature'),
    ('Gold Nugget', 'GoldNugget', 0, 2, None, 'terrain', 'nature'),
    ('Golden Pelt', 'Pelt_Golden', 0, 3, None, 'terrain', 'nature'),
    ('Rabbit Pelt', 'Pelt_Hare', 0, 1, None, 'terrain', 'nature'),
    ('Wolf Pelt', 'Pelt_Wolf', 0, 2, None, 'terrain', 'nature'),
    ('Ring Worm', 'RingWorm', 0, 1, 'blood_1', 'common', 'nature'),
    ('Stoat', 'Stoat', 1, 2, 'blood_1', 'common', 'nature'),
    ('The Smoke', 'Smoke', 0, 1, None, 'common', 'nature'),
    ('Greater Smoke', 'Smoke_Improved', 1, 3, None, 'common', 'nature'),
    ('Starvation', 'StarvingMan', None, None, None, 'common', 'nature'),
    ('Starvation', 'StarvingMan_Flight', None, None, None, 'common', 'nature'),
    ('Leaping Trap', 'Trap', 0, 1, None, 'terrain', 'nature'),
    ('Strange Frog', 'TrapFrog', 1, 2, 'blood_1', 'terrain', 'nature'),
    ('Frozen Opossum', 'Frozen_Opossum', 0, 5, None, 'terrain', 'nature'),
    ('Snowy Fir', 'Tree_SnowCovered', 0, 4, None, 'terrain', 'nature'),
    ('Grand Fir', 'Tree', 0, 3, None, 'terrain', 'nature'),
    ('Hungry Child', 'Child', 0, 0, None, 'common', 'nature'),
    ('Stump', 'Stump', 0, 3, None, 'terrain', 'nature'),
    ('AquaSquirrel', 'AquaSquirrel', 0, 1, None, 'common', 'nature'),
    ('Skeleton Crew', 'SkeletonPirate', 2, 1, None, 'common', 'nature'),
    ('Zombie Parrot', 'SkeletonParrot', 2, 3, None, 'common', 'nature'),
    ('Wild Bull', 'Bull', 3, 2, 'blood_2', 'common', 'nature'),
    ('Cuckoo', 'Cuckoo', 1, 1, 'blood_1', 'common', 'nature'),
    ('Ijiraq', 'Ijiraq', 4, 1, None, 'common', 'nature'),
    ('Flying Ant', 'AntFlying', None, 1, 'blood_1', 'common', 'nature'),
    ('Mud Turtle', 'MudTurtle_Shelled', 2, 2, 'blood_2', 'common', 'nature'),
    ('Mud Turtle', 'MudTurtle', 2, 2, 'blood_2', 'common', 'nature'),
    ('Dire Wolf Pup', 'DireWolfCub', 1, 1, 'blood_2', 'common', 'nature'),
    ('Dire Wolf', 'DireWolf', 2, 5, 'blood_3', 'common', 'nature'),
    ('Raccoon', 'Raccoon', 1, 1, 'blood_1', 'common', 'nature'),
    ('Lammergeier', 'Lammergeier', None, 4, 'blood_3', 'common', 'nature'),
    ('Red Hart', 'RedHart', None, 2, 'blood_2', 'common', 'nature'),
    ('Tadpole', 'Tadpole', 0, 1, None, 'common', 'nature'),
    ('Pelt Lice', 'Lice', 1, 1, 'blood_4', 'rare', 'nature'),
    ('Hodag', 'Hodag', 1, 5, 'blood_2', 'rare', 'nature'),
    ('Great Kraken', 'Kraken', 1, 1, 'blood_1', 'rare', 'nature'),
    ('Louis', 'Louis', 1, 1, 'blood_1', 'common', 'nature'),
    ('Kaycee', 'Kaycee', 1, 2, 'blood_1', 'common', 'nature'),
    # Bone Cards (Base Game)
    ('Alpha', 'Alpha', 1, 2, 'bone_4', 'common', 'nature'),
    ('Amoeba', 'Amoeba', 1, 2, 'bone_2', 'rare', 'nature'),
    ('Bat', 'Bat', 2, 1, 'bone_4', 'common', 'nature'),
    ('Cockroach', 'Cockroach', 1, 1, 'bone_4', 'common', 'nature'),
    ('Coyote', 'Coyote', 2, 1, 'bone_4', 'common', 'nature'),
    ('Corpse Maggots', 'Maggots', 1, 2, 'bone_5', 'common', 'nature'),
    ('Opossum', 'Opossum', 1, 1, 'bone_2', 'common', 'nature'),
    ('Rattler', 'Rattler', 3, 1, 'bone_6', 'common', 'nature'),
    ('Long Elk', 'LongElk', 1, 2, 'bone_4', 'rare', 'nature'),
    ('Stinkbug', 'Stinkbug_Talking', 1, 2, 'bone_2', 'common', 'nature'),
    ('Turkey Vulture', 'Vulture', 3, 3, 'bone_8', 'common', 'nature'),
    ('Mealworm', 'MealWorm', 0, 2, 'bone_2', 'common', 'nature'),
    ('Wolverine', 'Wolverine', 1, 3, 'bone_5', 'common', 'nature'),
    ('Curious Egg', 'HydraEgg', 0, 1, 'bone_1', 'rare', 'nature'),
    ('Hydra', 'Hydra', 1, 5, 'bone_1', 'rare', 'nature'),
    ('Reginald', 'Reginald', 1, 3, 'bone_3', 'common', 'nature'),
    ('Kaminski', 'Kaminski', 0, 1, 'bone_1', 'common', 'nature'),
    # Act 2 (nature)
    # ('Hrokkall', ),
    # ('Squirrel Ball', ),
    # ('Hawk', ),
    # ('Salmon', ),
    # ('Spore Mice', ),
    # ('Burrowing Trap', ),

    # Act 2 (undead)
    # ('Bone Heap', ),
    # ('Tomb Robber', ),
    # ('Necromancer', ),
    # ('Drowned Soul', ),
    # ('Dead Hand', ),
    # ('Headless Horseman', ),
    # ('Skeleton', ),
    # ('Draugr', ),
    # ('Gravedigger', ),
    # ('Sporedigger', ),
    # ('Banshee', ),
    # ('Skelemagus', ),
    # ('Zombie', ),
    # ("Bone Lord's Horn", ),
    # ('Broken Obol', ),
    # ('Broken Obol', ),
    # ('Repaired Obol', ),
    # ('Revenant', ),
    # ('Ghost Ship', ),
    # ('Sarcophagus', ),
    # ('The Walkers', ),
    # ('Frank & Stein', ),
    # ("Pharaoh's Pets", ),
    # ('Bonehound', ),
    # ('Mummy Lord', ),
    # ('Inspector', ),
    # ('Melter', ),

    # Act 2 (tech)
    # ('Plasma Jimmy', ),
    # ('Curve Hopper', ),
    # ('Energy Conduit', ),
    # ('Mox Module', ),
    # ('Mrs. Bomb', ),
    # ('Shutterbug', ),
    # ('L33pB0t', ),
    # ('Null Conduit', ),
    # ('Sentry Drone', ),
    # ('Sentry Spore', ),
    # ('49er', ),
    # ('Buff Conduit', ),
    # ('Energy Bot', ),
    # ('Explode Bot', ),
    # ('M3atB0t', ),
    # ('Automaton', ),
    # ('Factory Conduit', ),
    # ('Gamblobot', ),
    # ('Insectodrone', ),
    # ('Steel Mice', ),
    # ('Thick Droid', ),
    # ('Bolthound', ),
    # ('Double Gunner', ),
    # ('Steambot', ),

    # Act 2 (wizard)
    # TODO: Change from MagnificusMod portraits to other portraits - colored in images wont fit as well.
    # ('Magnus Mox', ),
    # ("Bleene's Mox", ),
    # ("Goranj's Mox", ),
    # ("Orlu's Mox", ),
    # ('Master Bleene', ),
    # ('Master Goranj', ),
    # ('Master Orlu', ),
    ('Emerald Mox', 'emeraldmox_splatter', 0, 1, None, 'common', 'wizard'),
    ('Ruby Mox', 'rubymox_splatter', 0, 1, None, 'common', 'wizard'),
    #TODO: Remove splatter from eyes as it looks bad (sapphire mox)
    ('Sapphire Mox', 'sapphiremox_splatter', 0, 1, None, 'common', 'wizard'),
    ('Mage Pupil', 'magepupil', 1, 1, None, 'common', 'wizard'),
    # ('Gourmage', ),
    # ('Green Mage', ),
    ('Junior Sage', 'juniorsage_splatter', 1, 2, '[green]', 'common', 'wizard'),
    # ('Muscle Mage', ),
    # ('Stim Mage', ),
    # ('Mage Knight', ),
    # ('Orange Mage', ),
    # ('Practice Wizard', ),
    # ('Ruby Golem', ),
    # ('Blue Mage', ),
    # ('Blue Sporemage', ),
    # ('Force Mage', ),
    # ('Gem Fiend', ),
    # ('Hover Mage', ),

    # Act 3
    # ('SON1A', ),
    # ('QU177', ),
    # ('GR1ZZ', ),
    # ('Bomb Latcher', ),
    # ('Exeskeleton', ),
    # ('Shield Latcher', ),
    # ('Skel-E-Latcher', ),
    # ('Gems Conduit', ),
    # ('Kind Cell', ),
    # ('Tough Cell', ),
    # ('Splinter Cell', ),
    # ("Bleene's Vessel", ),
    # ("Goranj's Vessel", ),
    # ("Orlu's Vessel", ),
    # ('Gem Detonator', ),
    # ('Gem Guardian', ),
    # ('Gembound Ripper', ),
    # ('Empty Vessel', ),
    # ('Emerald Vessel', ),
    # ('Ruby Vessel', ),
    # ('Sapphire Vessel', ),
    # ('Amoebot', ),
    # ('Gift Bot', ),
    # ('Lonely Wizbot', ),
    # ('Alarm Bot', ),
    # ('Busted 3D Printer', ),
    # ('Fishbot', ),
    # ('Insectodrone', ),
    # ('Shieldbot', ),
    # ('Sniper Bot', ),
    # ('Ourobot', ),
    # ('Swapbot', ),
    # ('Mycobot', ),
    # ('Bee', ),
    # ('Captive File', ),
    # ('Bad Fish', ),
    # ('More Fish', ),
    # ('Good Fish', ),
    # ('Dead Tree', ),
    # ('Annoy FM', ),
    # ('Bridge Rails', ),
    # ('Broken Bot', ),
    # ('Conduit Tower', ),
    # ('Tombstone', ),
    # ('Librarian', ),
    # ('The Daus', ),
]
for data in blood_card_data:
    cursor.execute('INSERT INTO cards (name, filename, power, health, cost, rarity, temple) VALUES (?, ?, ?, ?, ?, ?, ?)', data)

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
    ('Kaminski', 'base'),

    # Custom
    ('emeraldmox_splatter', 'axel'),
    ('rubymox_splatter', 'axel'),
    ('sapphiremox_splatter', 'axel'),
    ('magepupil', 'axel'),
    ('juniorsage_splatter', 'axel'),
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
    # Base Game
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
    # Custom Cards (From Act 2) - Axel
    ('emeraldmox_splatter', 'greenmox'),
    ('rubymox_splatter', 'orangemox'),
    ('sapphiremox_splatter', 'bluemox'),
    ('magepupil', 'gemdependant')
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


# Notes
note_data = [
    # Sigils
    ('madeofstone', 'sigils', 'A card bearing this sigil is immune to the effects of Touch of Death and Stinky.', None, None),
    ('drawrabbits', 'sigils', 'When a card bearing this sigil is played, a Rabbit is created in your hand. A Rabbit is defined as: 0 power, 1 health.', None, None),
    ('beesonhit', 'sigils', 'Once a card bearing this sigil is struck, a Bee is created in your hand. A Bee is defined as: 1 power, 1 health, airborne.', None, None),
    ('strafe', 'sigils', "At the end of the owner's turn, a card bearing this sigil will move in the direction inscribed in the sigil.", None, None),
    ('deathtouch', 'sigils', 'When a card bearing this sigil damages another creature, that creature perishes.', None, None),
    ('evolve', 'sigils', 'A card bearing this sigil will grow into a more powerful form after a specified amount of turns on the board.', None, None),
    ('evolve_1', 'sigils', 'A card bearing this sigil will grow into a more powerful form after 1 turn on the board.', None, None),
    ('evolve_2', 'sigils', 'A card bearing this sigil will grow into a more powerful form after 2 turns on the board.', None, None),
    ('evolve_3', 'sigils', 'A card bearing this sigil will grow into a more powerful form after 3 turns on the board.', None, None),
    ('createdams', 'sigils', 'When a card bearing this sigil is played, a Dam is created on each empty adjacent space. A Dam is defined as: 0 power, 2 health.', None, None),
    ('tutor', 'sigils', 'When a card bearing this sigil is played, you may search your deck for any card and take it into your hand.', None, None),
    ('whackamole', 'sigils', 'When an empty space would be struck, a card bearing this sigil will move to that space to receive the strike instead.', None, None),
    ('drawcopy', 'sigils', 'When a card bearing this sigil is played, a copy of it is created in your hand.', None, None),
    ('tailonhit', 'sigils', 'When a card bearing this sigil would be struck, a tail is created in its place and a card bearing this sigil moves to the right.', None, None),
    ('corpseeater', 'sigils', 'If a creature that you own perishes by combat, a card bearing this sigil in your hand is automatically played in its place.', None, None),
    ('quadruplebones', 'sigils', 'When a card bearing this sigil dies, 4 bones are awarded instead of 1.', None, None),
    ('submerge', 'sigils', "A card bearing this sigil submerges itself during its opponent's turn. While submerged, opposing creatures attack its owner directly.", None, None),
    ('drawcopyondeath', 'sigils', 'When a card bearing this sigil perishes, a copy of it is created in your hand.', None, None),
    ('sharp', 'sigils', 'Once a card bearing this sigil is struck, the striker is then dealt a single damage point.', None, None),
    ('strafepush', 'sigils', "At the end of the owner's turn, a card bearing this sigil will move in the direction inscribed in the sigil. Creatures in the way will be pushed in the same direction.", None, None),
    ('strafeswap', 'sigils', "At the end of the owner's turn, a card bearing this sigil will move in the direction inscribed in the sigil. Creatures in the way will be thrown back behind it.", None, None),
    ('createegg', 'sigils', 'When a card bearing this sigil is played, an egg is created on the opposing space.', None, None),
    ('deathshield', 'sigils', 'The first time a card bearing this sigil would take damage, prevent that damage.', None, None),
    ('doublestrike', 'sigils', 'A card bearing this sigil will strike the opposing space an extra time when attacking.', None, None),
    ('morsel', 'sigils', 'When a card bearing this sigil is sacrificed, it adds its stat values to the card it was sacrificed for.', None, None),
    ('gainattackonkill', 'sigils', 'When a card bearing this sigil attacks an opposing creature and it perishes, this card gains 1 power.', None, None),
    ('opponentbones', 'sigils', 'When a card bearing this sigil is on the board, opposing creatures also provide bones when perishing.', None, None),
    ('hydraegg', 'sigils', 'A card bearing this sigil hatches when drawn if the numbers 1 to 5 are represented in the health of creatures in your deck, and in their power, and if there is a creature of each tribe in your deck.', None, None),
    ('drawant', 'sigils', 'When a card bearing this sigil is played, an ant is created in your hand.', None, None),
    ('guarddog', 'sigils', 'When an opposing creature is placed opposite to an empty space, a card bearing this sigil will move to that empty space.', None, None),
    ('flying', 'sigils', 'A card bearing this sigil will strike an opponent directly, even if there is a creature opposing it.', None, None),
    ('sacrificial', 'sigils', 'When a card bearing this sigil is sacrificed it does not perish.', None, None),
    ('preventattack', 'sigils', 'If a creature would attack a card bearing this sigil, it does not.', None, None),
    ('tripleblood', 'sigils', 'A card bearing this sigil is counted as 3 blood rather than 1 blood when sacrificed. ', None, None),
    ('reach', 'sigils', 'A card bearing this sigil will block an opposing creature bearing the airborne sigil.', None, None),
    ('splitstrike', 'sigils', 'A card bearing this sigil will strike each opposing space to the left and right of the space across from it.', None, None),
    ('tristrike', 'sigils', 'A card bearing this sigil will strike each opposing space to the left, right, and center of it.', None, None),
    ('icecube', 'sigils', 'When a card bearing this sigil perishes, the creature inside is released in its place.', None, None),
    ('sinkhole', 'sigils', "At the end of the owner's turn, opposing cards will move towards a card bearing this sigil. The card directly opposing a card bearing this sigil will perish at the end of the owner's turn.", None, None),
    ('bonedigger', 'sigils', "At the end of the owner's turn, a card bearing this sigil will generate 1 bone.", None, None),
    ('randomconsumable', 'sigils', 'When a card bearing this sigil is played, you will receive a random item as long as your pack is not full.', None, None),
    ('steeltrap', 'sigils', 'When a card bearing this sigil perishes, the creature opposing it perishes as well. A pelt is created in your hand.', None, None),
    ('randomability', 'sigils', 'When a card bearing this sigil is drawn, this sigil is replaced with another sigil at random.', None, None),
    ('squirrelorbit', 'sigils', "At the beginning of its owner's turn, a card bearing this sigil will pull small creatures, like squirrels, into its orbit.", None, None),
    ('allstrike', 'sigils', 'A card bearing this sigil will strike each opposing space that is occupied by a creature. It will strike directly if no creatures oppose it.', None, None),
    ('buffneighbours', 'sigils', 'Creatures adjacent to a card bearing this sigil gain 1 power.', None, None),
    ('brittle', 'sigils', 'After attacking, a card bearing this sigil perishes.', None, None),
    ('skeletonstrafe', 'sigils', "At the end of the owner's turn, a card bearing this sigil will move in the direction inscribed in the sigil and drop a Skeleton in its old space.", None, None),
    ('greenmox', 'sigils', 'While a card bearing this sigil is on the board, it provides a Green Gem to its owner.', None, None),
    ('orangemox', 'sigils', 'While a card bearing this sigil is on the board, it provides an Orange Gem to its owner.', None, None),
    ('bluemox', 'sigils', 'While a card bearing this sigil is on the board, it provides a Blue Gem to its owner.', None, None),
    ('buffgems', 'sigils', "While a card bearing this sigil is on the board, Mox Cards on the owner's side of the board gain 1 power.", None, None),
    ('droprubyondeath', 'sigils', 'When a card bearing this sigil perishes, a Ruby Mox is created in its place.', None, None),
    ('gemsdraw', 'sigils', 'When a card bearing this sigil is played, you draw cards equal to the amount of Mox Cards on your side of the board.', None, None),
    ('gemdependant', 'sigils', "If a card bearing this sigil's owner controls no Mox Cards, a card bearing this sigil perishes.", None, None),
    ('gaingemtriple', 'sigils', 'While a card bearing this sigil is on the board, it provides a Green, Orange, and Blue Gem to its owner.', None, None),
    ('drawnewhand', 'sigils', 'When a card bearing this sigil is played, discard your hand then draw a new hand of 4 cards.', None, None),
    ('squirrelstrafe', 'sigils', "At the end of the owner's turn, a card bearing this sigil will move in the direction inscribed in the sigil and drop a Squirrel in their old space" , None, None),
    ('conduitbuffattack', 'sigils', 'Other creatures within a circuit completed by a card bearing this sigil gain 1 power.', None, None),
    ('conduitfactory', 'sigils', "Empty spaces within a circuit completed by a card bearing this sigil spawn L33pB0ts at the end of the owner's turn.", None, None),
    ('conduitheal', 'sigils', "Other creatures within a circuit completed by a card bearing this sigil are healed by 1 at the end of the owner's turn.", None, None),
    ('conduitnull', 'sigils', 'A card bearing this sigil may complete a circuit, but provides no effect.', None, None),
    ('gainbattery', 'sigils', 'When a card bearing this sigil is played, it provides an Energy Cell to its owner.', None, None),
    ('explodeondeath', 'sigils', 'When a card bearing this sigil dies, the creature opposing it, as well as adjacent friendly creatures, are dealt 10 damage.', None, None),
    ('sniper', 'sigils', 'You may choose which opposing space a card bearing this sigil strikes.', None, None),
    ('deathshield_nano', 'sigils', 'The first time a card bearing this sigil would take damage, prevent that damage.', None, None),
    ('permadeath', 'sigils', 'A card bearing this sigil has increased power. But, if a card bearing this sigil perishes, it is permanently removed from your deck.', None, None),
    ('latchexplodeondeath', 'sigils', 'When a card bearing this sigil perishes, its owner chooses a creature to gain the Detonator sigil.', None, None),
    ('latchbrittle', 'sigils', 'When a card bearing this sigil perishes, its owner chooses a creature to gain the Brittle sigil.', None, None),
    ('latchdeathshield', 'sigils', 'When a card bearing this sigil perishes, its owner chooses a creature to gain the Nano Armor sigil.', None, None),
    ('filesizedamage', 'sigils', "When a card bearing this sigil perishes, select an object. Place damage on the scales according to the object's size.", None, None),
    ('deletefile', 'sigils', 'When a card bearing this sigil perishes, it is permanently removed from your deck.', None, None),
    ('transformer', 'sigils', 'At the beginning of your turn a card bearing this sigil will transform to, or from, Beast mode.', None, None),
    ('sentry', 'sigils', 'When a creature moves into the space opposing a card bearing this sigil, they are dealt 1 damage.', None, None),
    ('explodegems', 'sigils', "When Gem Vessels on the owner's side of the board die, they detonate (the creature opposing them, as well as adjacent friendly creatures, are dealt 10 damage).", None, None),
    ('shieldgems', 'sigils', "When a card bearing this sigil is played, all Gem Vessels on the owners' side of the board gain Nano Armor.", None, None),
    ('drawvesselonhit', 'sigils', 'Once a card bearing this sigil is struck, draw a card from your Empty Vessel pile.', None, None),
    ('conduitenergy', 'sigils', 'If a card bearing this sigil is part of a completed circuit, your Energy never depletes.', None, None),
    ('bombspawner', 'sigils', 'When a card bearing this sigil is played, fill all empty spaces with Explode Bots.', None, None),
    ('doubledeath', 'sigils', 'When another creature you own dies, it is returned to life and dies again immediately.', None, None),
    ('activatedrandompowerenergy', 'sigils', 'Activate: Pay 1 Energy to set the power of a card bearing this sigil randomly between 1 and 6.', None, None),
    ('activatedstatsup', 'sigils', 'Activate: Pay 2 Bones to increase the power and health of a card bearing this sigil by 1.', None, None),
    ('swapstats', 'sigils', 'After a card bearing this sigil is dealt damage, swap its Power and Health.', None, None),
    ('activateddrawskeleton', 'sigils', 'Activate: Pay 1 Bone to create a Skeleton in your hand.', None, None),
    ('activateddealdamage', 'sigils', 'Activate: Pay 1 Energy to deal 1 damage to the creature across from a card bearing this sigil.', None, None),
    ('createbells', 'sigils', 'When a card bearing this sigil is played, a Chime is created on each empty adjacent space. A Chime is defined as: 0 power, 1 health.', None, None),
    ('buffenemy', 'sigils', 'The creature opposing a card bearing this sigil gains 1 power.', None, None),
    ('conduitspawngems', 'sigils', "Empty spaces within a circuit completed by a card bearing this sigil spawn Gem Vessels at the end of the owner's turn.", None, None),
    ('drawrandomcardondeath', 'sigils', 'When a card bearing this sigil perishes, a random card is created in your hand.', None, None),
    ('loot', 'sigils', 'When a card bearing this sigil deals damage directly, draw a card for each damage dealt.', None, None),
    ('activatedsacrificedrawcards', 'sigils', 'Activate: If you have a Blue Gem, sacrifice a card bearing this sigil to draw 3 cards.', None, None),
    ('activatedstatsupenergy', 'sigils', 'Activate: Pay 3 Energy to increase the power and health of a card bearing this sigil by 1.', None, None),
    ('activatedheal', 'sigils', 'Activate: Pay 2 Bones to heal a card bearing this sigil by 1.', None, None),
    ('debuffenemy', 'sigils', 'The creature opposing a card bearing this sigil loses 1 power.', None, None),
    ('cellbuffself', 'sigils', 'If a card bearing this sigil is within a circuit, it gains 2 power.', None, None),
    ('celldrawrandomcardondeath', 'sigils', 'If a card bearing this sigil is within a circuit when it perishes, a random card is created in your hand.', None, None),
    ('celltristrike', 'sigils', 'If a card bearing this sigil is within a circuit, it will strike each opposing space to the left, right, and center of it.', None, None),
    ('activatedenergytobones', 'sigils', 'Activate: Pay 1 Energy to gain 3 Bones.', None, None),
    ('movebeside', 'sigils', 'When one of your creatures is placed in a space, a card bearing this sigil will move towards them as far as possible.', None, None),
    ('submergesquid', 'sigils', "A card bearing this sigil submerges itself during its opponent's turn. While submerged, opposing creatures attack its owner directly.", None, None),
    ('bloodguzzler', 'sigils', 'When a creature bearing this sigil deals damage, it gains 1 health for each damage dealt.', None, None),
    ('haunter', 'sigils', 'When a creature bearing this sigil dies, it haunts the space it died in. Creatures played on this space gain its old sigils.', None, None),
    ('explodingcorpse', 'sigils', 'When a creature bearing this sigil dies, all empty spaces on the board are filled with a Guts card.', None, None),
    ('bloodymary', 'sigils', "A creature bearing this sigil gains 1 power when you speak 'Bloody Mary' up to a total of 13 times.", None, None),
    ('virtualreality', 'sigils', "If a card bearing this sigil's owner owns a VR Headset, a card bearing this sigil may be played without paying its cost.", None, None),
    ('edaxiohead', 'sigils', 'Edaxio is summoned if you control creatures bearing the sigils of Head, Arms, Legs, and Torso of Edaxio.', None, None),
    ('edaxioarms', 'sigils', 'Edaxio is summoned if you control creatures bearing the sigils of Head, Arms, Legs, and Torso of Edaxio.', None, None),
    ('edaxiolegs', 'sigils', 'Edaxio is summoned if you control creatures bearing the sigils of Head, Arms, Legs, and Torso of Edaxio.', None, None),
    ('edaxiotorso', 'sigils', 'Edaxio is summoned if you control creatures bearing the sigils of Head, Arms, Legs, and Torso of Edaxio.', None, None),
    # Stat Icons
    ('ants', 'staticons', 'The value represented with this sigil will be equal to the number of Ants that the owner has on their side of the table.', None, None),
    ('sacrifices', 'staticons', 'The value represented with this sigil will be equal to the number of sacrifices made during your turn.', None, None),
    ('bell', 'staticons', 'The value represented with this sigil will be equal to 4 minus the distance of the creature bearing it to the combat bell.', None, None),
    ('cardsinhand', 'staticons', 'The value represented with this sigil will be equal to the number of cards in your hand.', None, None),
    ('mirror', 'staticons', 'The value represented with this sigil will be equal to that of the creature opposing the creature with this sigil.', None, None),
    ('bones', 'staticons', 'The value represented with this sigil will be equal to half the number of bone tokens owned by the owner of the creature with this sigil.', None, None),
    ('greengems', 'staticons', 'The value represented with this sigil will be equal to the number of Green Gems that the owner has on their side of the table.', None, None),
    # Boons
    ('startinggoat', 'boons', 'You will start a battle with a Black Goat on the board.', None, None),
    ('doubledraw', 'boons', 'You may draw twice at the beginning of your turn.', None, None),
    ('startingbones', 'boons', 'You will start a battle with 8 Bones.', None, None),
    ('startingtrees', 'boons', 'You will start a battle with Grand Firs on all of your spaces.', None, None),
    ('tutordraw', 'boons', 'When you draw from your deck, you may choose any card in your deck to draw.', None, None),
    ('singlestartingbone', 'boons', 'You will start each battle with 1 extra Bone.', None, None),
    # Items
    ('goatbottle', 'items', 'To the user: A Black Goat is created in your hand. A Black Goat is defined as: 0 Power, 1 Health, Worthy Sacrifice.', None, None),
    ('terrainbottle', 'items', 'To the user: A Boulder is created in your hand. A Boulder is defined as: 0 Power, 5 Health.', None, None),
    ('goobottle', 'items', 'To the user: Nothing will happen. This bottle of goo has no use.', None, None),
    ('fishhook', 'items', 'To the user: Hook one of my cards and take it as your own. You must have an empty space on your side to receive it.', None, None),
    ('frozenopossumbottle', 'items', 'To the user: A Frozen Opossum is created in your hand. A Frozen Opossum is defined as: 0 Power, 5 Health, Frozen Away.', None, None),
    ('birdlegfan', 'items', 'To the user: Your creatures will attack as though they have the Airborne Sigil this turn.', None, None),
    ('piggybank', 'items', 'To the user: You will immediately gain 4 Bones.', None, None),
    ('hourglass', 'items', 'To the user: Your adversary will entirely skip their next turn.', None, None),
    ('bleachpot', 'items', 'To the user: My cards on the board will lose all of their sigils.', None, None),
    ('magnifyingglass', 'items', 'To the user: You will search your deck for any card and take it into your hand.', None, None),
    ('pliers', 'items', 'To the user: You will place a weight on the scales. The pain is temporary.', None, None),
    ('scissors', 'items', "To the user: You may cut up one of your adversary's cards. It is destroyed.", None, None),
    ('trapperknife', 'items', "To the user: You may skin one of your adversary's cards. It is destroyed and you draw a pelt card.", None, None),
    ('specialdagger', 'items', 'To the user: You will place a weight on the scales. The pain is temporary.', None, None),
    ('squirrelbottle', 'items', 'To the user: A Squirrel is created in your hand. A Squirrel is defined as: 0 Power, 1 Health.', None, None),
    ('pocketwatch', 'items', 'To the user: All creatures on the board will rotate one space clockwise.', None, None),
    ('Extra Battery', 'items', "Replenishes Energy back up to the current maximum. It's alright.", None, None),
    ("Mrs. Bomb's Remote", 'items', 'Places Explode Bots on all empty spaces. Pretty annoying honestly.', None, None),
    ('Nano Armor Generator', 'items', "Your bots on the board get Nano Armor. If you use it right it's decently OK.", None, None),
    # Spells
]
for data in note_data:
    cursor.execute('INSERT INTO notes (filename, type, description, mechanics, gmNotes) VALUES (?, ?, ?, ?, ?)', data)

# Commit and disconnect
conn.commit()
conn.close()

print("Database 'inscryption.db' initialized.")
