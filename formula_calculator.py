from card import Card
from helpers import db_connect

BONE_VALUE = (3.0 / 2.5)
ENERGY_VALUE = 1.0
BLOOD_VALUE = {
    0: 0,
    1: 3,
    2: 8,
    3: 14,
    4: 21
}
GEM_VALUE = {
    0: 0,
    1: 2,
    2: 5,
    3: 8
}

def get_stats_value(card, stat):
    value = 0
    if card.stats[stat] is not None:
        value = card.stats[stat]
    return value

def get_cost_value(card, cost):
    value = 0
    if card.costs[cost] is not None:
        value = card.costs[cost]
    return value

@db_connect
def calculate_balance(cursor):
    # SELECT and fetch to retrieve all cards from table
    cursor.execute('SELECT * FROM cards')
    rows = cursor.fetchall()

    # Checking balance of all cards
    for row in rows:
        stat_points_spent = 0
        card = Card(*row)

        print(card.name + ': ')
        # Get value of card - ie how many points can be spent for attack, health, sigils, etc.
        blood = get_cost_value(card, 'blood')
        bone = get_cost_value(card, 'bone')
        energy = get_cost_value(card, 'energy')
        orange = get_cost_value(card, 'orange')
        green = get_cost_value(card, 'green')
        blue = get_cost_value(card, 'blue')
        stat_point_value = BLOOD_VALUE[blood] +\
                           BONE_VALUE * bone +\
                           ENERGY_VALUE * energy +\
                           GEM_VALUE[orange + green + blue]
        if stat_point_value == 0:
            stat_point_value = 1

        # Get amount of points spent on card - ie the more powerful the card is, the more points were obviously spent on it.
        power = get_stats_value(card, 'power')
        health = get_stats_value(card, 'health')

        cursor.execute(f'SELECT * FROM card_sigils WHERE card_filename = ?', (card.filename,))
        sigils = cursor.fetchall()
        for sigil in sigils:
            stat_points_spent += sigil[2]

        stat_points_spent = (power * 2) + health
        if card.types['rarity'] == 'rare' or '_Talking' in card.filename:
            stat_points_spent += 1


        print('Card Value: '+str(stat_point_value))
        print('Card Power: '+str(float(stat_points_spent)))
        print('Point Surplus/Shortage: '+str(int(stat_point_value - stat_points_spent))+'\n')


if __name__ == '__main__':
    calculate_balance()




# BALANCING FORMULA
# O RESOURCES = 1 Stat Point
# 1 GEM PLACED = 2 Stat Points
# 2 GEMS PLACED = 5 Stat Points
# 1 BLOOD = 2.5 BONES = 3 ENERGY = 1.5 GEMS PLACED = 3 Stat Points
# 5 BONES = 6 ENERGY = 6 Stat Points
# 2 BLOOD = 3 GEMS PLACED = 8 Stat Points
# 3 BLOOD = 14 Stat Points
# 4 BLOOD = 21 Stat Points
# GEM DEPENDENT = 3 Stat Points
# Stat Points = Power * 2 + Toughness + Power Levels of Abilities +/- 1 (flexibility) + 1 for Rare or Talking cards.