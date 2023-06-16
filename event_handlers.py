from enum import Enum
from choice_handlers import rest_continue
from dungeon_room import randint, Room
from character import Party, Enemy


class PlayerChoiceEnum(Enum):
    UNKNOWN = 0
    REST = 1
    CONTINUE = 2
    LEAVE = 3

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class DungeonEnum(Enum):
    LOOT = 1
    COMBAT = 2


class SearchEum(Enum):
    DUNGEON = 1
    LOST = 2


def search_for_entrance(player: Party) -> bool:
    dungeon_chance = randint(1, 10)
    if dungeon_chance > 6:
        return True
    elif dungeon_chance > 2 and player.expertise is True:  # do the method thing
        return True
    else:
        return False


def search_for_dungeon(player: Party):
    continue_exploration = True
    dungeon_found = False
    while continue_exploration and not dungeon_found and player.has_supplies():
        player.spend_mp()
        dungeon_found = search_for_entrance(player)
        continue_exploration = rest_continue(player)


def explore_dungeon(player: Party):
    continue_exploration = True
    while continue_exploration and player.is_alive() and player.has_supplies():
        room = Room.random()
        handle_room(player, room)
        continue_exploration = rest_continue(player)
    if not player.is_alive():
        player.lose_treasure()


def get_dungeon_room() -> 'Room':
    return Room.random()


def handle_room(player: Party, room: Room):
    player.spend_mp()
    if room.get_monster() is not None:
        handle_combat(player, room.get_monster())
    player.add_loot(room.loot_value)
    if room.loot_value == 900 and player.expertise is True:
        player.add_loot(200)


def handle_combat(player: Party, monster: Enemy):
    player.spend_mp()
    while player.is_alive() and monster.is_alive():
        player.lose_hp(monster.damage)
        monster.lose_hp(player.damage)
