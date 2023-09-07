import re

from printer import get_data, call_database
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

def get_power_value(card):
    value = 0
    if card.power is not None:
        value = card.power
    return value

def get_health_value(card):
    value = 0
    if card.health is not None:
        value = card.health
    return value

def get_cost_value(card, cost):
    value = 0
    if card.costs[cost] is not None:
        value = card.costs[cost]
    return value

@db_connect
def calculate_balance(cursor):
    cards = call_database(True, 'SELECT * FROM cards')

    # Checking balance of all cards
    for data in cards:
        stat_points_spent = 0
        card_data = dict(data)
        filename = card_data["filename"]
        tribe_data = get_data('card_tribes', filename)
        sigil_data = get_data('card_sigils', filename)
        flag_data = get_data('card_flags', filename)
        decal_data = get_data('card_decals', filename)
        before_decal_data = get_data('card_before_decals', filename)
        deathcard_data = get_data('death_cards', filename)
        deathcard_data = deathcard_data[0] if len(deathcard_data) == 1 else None
        staticon_data = get_data('card_staticons', filename)
        category_data = get_data('card_categories', filename)[0]['category']

        card = Card(cursor, './', card_data, tribe_data, sigil_data, flag_data,
                    before_decal_data, decal_data, deathcard_data, staticon_data, category_data)

        print(card.name + ': ')
        # Get value of card - ie how many points can be spent for attack, health, sigils, etc.
        cost_map = {
            'blood': 0,
            'bone': 0,
            'energy': 0,
            'gem': 0,
        }
        if card.cost == None:
            pass
        elif card.cost[0] != '[':
            cost_map[f'{card.cost.split("_")[0]}'] = int(card.cost.split("_")[1])
        else:
            for cost in re.findall(r'\[(.*?)\]', card.cost):
                if cost not in ('blood', 'bone', 'energy'):
                    cost_map['gem'] += 1
                else:
                    cost_map[cost] += 1
        stat_point_value = BLOOD_VALUE[cost_map['blood']] +\
                           BONE_VALUE * cost_map['bone'] +\
                           ENERGY_VALUE * cost_map['energy'] +\
                           GEM_VALUE[cost_map['gem']]
        if stat_point_value == 0:
            stat_point_value = 1

        # Get amount of points spent on card - ie the more powerful the card is, the more points were obviously spent on it.
        power = get_power_value(card)
        health = get_health_value(card)

        cursor.execute(f'SELECT * FROM card_sigils WHERE card_filename = ?', (card.filename,))
        sigils = cursor.fetchall()
        for sigil in sigils:
            stat_points_spent += sigil[2]

        stat_points_spent = (power * 2) + health
        if card.rarity == 'rare' or '_Talking' in card.filename:
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