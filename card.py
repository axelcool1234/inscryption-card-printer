from helpers import db_connect

class Card:
    def __init__(self, name, filename,
                 power, health,
                 bloodCost, boneCost, energyCost, orangeMoxCost, greenMoxCost, blueMoxCost,
                 rarity, temple, note_id):
        self.name = name
        self.filename = filename
        self.stats = {
            'power': power,
            'health': health
        }
        self.costs = {
            'bloodCost': bloodCost,
            'boneCost': boneCost,
            'energyCost': energyCost,
            'orangeMoxCost': orangeMoxCost,
            'greenMoxCost': greenMoxCost,
            'blueMoxCost': blueMoxCost
        }
        self.types = {
            'rarity': rarity,
            'temple': temple
        }
        if note_id is None:
            self.notes = None
        else:
            self.notes = self.get_notes_from_database(note_id)

    @db_connect
    def get_notes_from_database(self, cursor, note_id):
        # SELECT query and fetch to retrieve notes based on note_id
        cursor.execute('SELECT description, mechanics, gmNotes FROM notes WHERE id = ?', (note_id,))
        row = cursor.fetchone()
        # Assign notes to card
        if row:
            description, mechanics, gmNotes = row
            return {
                'description': description,
                'mechanics': mechanics,
                'gmNotes': gmNotes
            }
        else:
            return None