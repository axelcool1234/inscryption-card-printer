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
    #('Green Gems', 'greengems',)
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
    #('Skeleton Crew', 'skeletonstrafe', 3),
    ('Green Mox', 'greenmox', 2),
    ('Orange Mox', 'orangemox', 2),
    ('Blue Mox', 'bluemox', 2),
    ('Gem Animator', 'buffgems', 3),
    ('Ruby Heart', 'droprubyondeath', 3),
    ('Mental Gemnastics', 'gemsdraw', 3),
    ('Gem Dependant', 'gemdependant', -3),
    #('Great Mox', 'gaingemtriple', 4),
    #('Handy', 'drawnewhand', 4),
    #('Squirrel Shedder', 'squirrelstrafe', 3),
    ('Attack Conduit', 'conduitbuffattack', 3),
    #('Spawn Conduit', 'conduitfactory', 3),
    #('Healing Conduit', 'conduitheal', 5),
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
    #('Energy Conduit', 'conduitenergy', 2),
    #('Bomb Spewer', 'bombspawner', 4),
    #('Double Death', 'doubledeath', 3),
    #('Bone Dice', 'activatedrandompowerenergy', 3),
    #('Enlarge', 'activatedstatsup', 4),
    ('Swapper', 'swapstats', 0),
    #('Disentomb', 'activateddrawskeleton', 3),
    #('Energy Gun', 'activateddealdamage', 4),
    ('Bellist', 'createbells', 4),
    ('Annoying', 'buffenemy', -1),
    ('Gem Spawn Conduit', 'conduitspawngems', 3),
    ('Gift Bearer', 'drawrandomcardondeath', 3),
    #('Looter', 'loot', 4),
    #('True Scholar', 'activatedsacrificedrawcards', 3),
    #('Stimulate', 'activatedstatsupenergy', 4),
    #('Marrow Sucker', 'activatedheal', 1),
    ('Stinky', 'debuffenemy', 2),
    ('Buff When Powered', 'cellbuffself', 2),
    ('Gift When Powered', 'celldrawrandomcardondeath', 1),
    ('Trifurcated When Powered', 'celltristrike', 3),
    #('Bonehorn', 'activatedenergytobones', 4),
    ('Clinger', 'movebeside', 0),
    ('Kraken Waterborne', 'submergesquid', 2),
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
    # Mox Cards (from Act 2) - Axel
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
    ('madeofstone', 'sigils', None, None, None),
    ('drawrabbits', 'sigils', None, None, None),
    ('beesonhit', 'sigils', None, None, None),
    ('strafe', 'sigils', None, None, None),
    ('deathtouch', 'sigils', None, None, None),
    ('evolve', 'sigils', None, None, None),
    ('evolve_1', 'sigils', None, None, None),
    ('evolve_2', 'sigils', None, None, None),
    ('evolve_3', 'sigils', None, None, None),
    ('createdams', 'sigils', None, None, None),
    ('tutor', 'sigils', None, None, None),
    ('whackamole', 'sigils', None, None, None),
    ('drawcopy', 'sigils', None, None, None),
    ('tailonhit', 'sigils', None, None, None),
    ('corpseeater', 'sigils', None, None, None),
    ('quadruplebones', 'sigils', None, None, None),
    ('submerge', 'sigils', None, None, None),
    ('drawcopyondeath', 'sigils', None, None, None),
    ('sharp', 'sigils', None, None, None),
    ('strafepush', 'sigils', None, None, None),
    ('strafeswap', 'sigils', None, None, None),
    ('createegg', 'sigils', None, None, None),
    ('deathshield', 'sigils', None, None, None),
    ('doublestrike', 'sigils', None, None, None),
    ('morsel', 'sigils', None, None, None),
    ('gainattackonkill', 'sigils', None, None, None),
    ('opponentbones', 'sigils', None, None, None),
    ('hydraegg', 'sigils', None, None, None),
    ('drawant', 'sigils', None, None, None),
    ('guarddog', 'sigils', None, None, None),
    ('flying', 'sigils', None, None, None),
    ('sacrificial', 'sigils', None, None, None),
    ('preventattack', 'sigils', None, None, None),
    ('tripleblood', 'sigils', None, None, None),
    ('reach', 'sigils', None, None, None),
    ('splitstrike', 'sigils', None, None, None),
    ('tristrike', 'sigils', None, None, None),
    ('icecube', 'sigils', None, None, None),
    ('sinkhole', 'sigils', None, None, None),
    ('bonedigger', 'sigils', None, None, None),
    ('randomconsumable', 'sigils', None, None, None),
    ('steeltrap', 'sigils', None, None, None),
    ('randomability', 'sigils', None, None, None),
    ('squirrelorbit', 'sigils', None, None, None),
    ('allstrike', 'sigils', None, None, None),
    ('buffneighbours', 'sigils', None, None, None),
    ('brittle', 'sigils', None, None, None),
    ('skeletonstrafe', 'sigils', None, None, None),
    ('green_mox', 'sigils', None, None, None),
    ('orange_mox', 'sigils', None, None, None),
    ('blue_mox', 'sigils', None, None, None),
    ('buffgems', 'sigils', None, None, None),
    ('droprubyondeath', 'sigils', None, None, None),
    ('gemsdraw', 'sigils', None, None, None),
    ('gem_dependant', 'sigils', None, None, None),
    ('gaingemtriple', 'sigils', None, None, None),
    ('drawnewhand', 'sigils', None, None, None),
    ('squirrelstrafe', 'sigils', None, None, None),
    ('conduitbuffattack', 'sigils', None, None, None),
    ('conduitfactory', 'sigils', None, None, None),
    ('conduitheal', 'sigils', None, None, None),
    ('conduitnull', 'sigils', None, None, None),
    ('gainbattery', 'sigils', None, None, None),
    ('explodeondeath', 'sigils', None, None, None),
    ('sniper', 'sigils', None, None, None),
    ('deathshield_nano', 'sigils', None, None, None),
    ('permadeath', 'sigils', None, None, None),
    ('latchexplodeondeath', 'sigils', None, None, None),
    ('latchbrittle', 'sigils', None, None, None),
    ('latchdeathshield', 'sigils', None, None, None),
    ('filesizedamage', 'sigils', None, None, None),
    ('deletefile', 'sigils', None, None, None),
    ('transformer', 'sigils', None, None, None),
    ('sentry', 'sigils', None, None, None),
    ('explodegems', 'sigils', None, None, None),
    ('shieldgems', 'sigils', None, None, None),
    ('drawvesselonhit', 'sigils', None, None, None),
    ('conduitenergy', 'sigils', None, None, None),
    ('bombspawner', 'sigils', None, None, None),
    ('doubledeath', 'sigils', None, None, None),
    ('activatedrandompowerenergy', 'sigils', None, None, None),
    ('activatedstatsup', 'sigils', None, None, None),
    ('swapstats', 'sigils', None, None, None),
    ('activateddrawskeleton', 'sigils', None, None, None),
    ('activateddealdamage', 'sigils', None, None, None),
    ('createbells', 'sigils', None, None, None),
    ('buffenemy', 'sigils', None, None, None),
    ('conduitspawngems', 'sigils', None, None, None),
    ('drawrandomcardondeath', 'sigils', None, None, None),
    ('loot', 'sigils', None, None, None),
    ('activatedsacrificedrawcards', 'sigils', None, None, None),
    ('activatedstatsupenergy', 'sigils', None, None, None),
    ('activatedheal', 'sigils', None, None, None),
    ('debuffenemy', 'sigils', None, None, None),
    ('cellbuffself', 'sigils', None, None, None),
    ('celldrawrandomcardondeath', 'sigils', None, None, None),
    ('celltristrike', 'sigils', None, None, None),
    ('activatedenergytobones', 'sigils', None, None, None),
    ('movebeside', 'sigils', None, None, None),
    ('submergesquid', 'sigils', None, None, None),
    ('bloodguzzler', 'sigils', None, None, None),
    ('haunter', 'sigils', None, None, None),
    ('explodingcorpse', 'sigils', None, None, None),
    ('bloodymary', 'sigils', None, None, None),
    ('virtualreality', 'sigils', None, None, None),
    ('edaxiohead', 'sigils', None, None, None),
    ('edaxioarms', 'sigils', None, None, None),
    ('edaxiolegs', 'sigils', None, None, None),
    ('edaxiotorso', 'sigils', None, None, None),
    # Stat Icons
    ('ants', 'staticons', None, None, None),
    ('sacrifices', 'staticons', None, None, None),
    ('bell', 'staticons', None, None, None),
    ('cardsinhand', 'staticons', None, None, None),
    ('mirror', 'staticons', None, None, None),
    ('bones', 'staticons', None, None, None),
    ('greengems', 'staticons', None, None, None),
    # Boons

    # Items

    # Spells
]
for data in note_data:
    cursor.execute('INSERT INTO notes (filename, type, description, mechanics, gmNotes) VALUES (?, ?, ?, ?, ?)', data)

# Commit and disconnect
conn.commit()
conn.close()

print("Database 'inscryption.db' initialized.")
