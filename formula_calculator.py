from card import Card
from helpers import db_connect
@db_connect
def calculate_balance(cursor):
    # SELECT and fetch to retrieve all cards from table
    cursor.execute('SELECT * FROM cards')
    rows = cursor.fetchall()

    # Generating all cards
    for row in rows:
        card = Card(*row)

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