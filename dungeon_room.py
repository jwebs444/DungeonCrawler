from character import Enemy
from random import randint


def _loot_value():
    dungeon_loot_chance = randint(1, 6)
    if dungeon_loot_chance == 1:
        dungeon_room_loot = 0
    elif dungeon_loot_chance == 2:
        dungeon_room_loot = 100
    elif dungeon_loot_chance == 3:
        dungeon_room_loot = 250
    elif dungeon_loot_chance == 4:
        dungeon_room_loot = 500
    elif dungeon_loot_chance == 5:
        dungeon_room_loot = 750
    else:
        dungeon_room_loot = 900
    return dungeon_room_loot


def _random_enemy():
    has_monster = randint(1, 10) > 6

    if has_monster:
        room_hp = randint(10, 20)
        room_dam = randint(1, 10)
        return Enemy(room_hp, room_dam)
    return None


class Room:
    def __init__(self, monster: Enemy, loot_value: int):
        self.monster: Enemy = monster
        self.loot_value: int = loot_value

    def get_monster(self) -> Enemy:
        return self.monster

    def get_loot_value(self) -> int:
        return self.loot_value

    @staticmethod
    def random() -> 'Room':
        return Room(_random_enemy(), _loot_value())
