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


class BaseInterface:
    def write(self, message: str):
        raise NotImplementedError

    def input(self, message: str) -> str:
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError


# Turn this into a class where terminal output is wiped between "screens"
# Stop it from being a scroller forever, and have one dialog window visible at a time
# Look into carriage return and flush
class TerminalInterface(BaseInterface):
    def write(self, message: str):
        print(message)
        return message

    def input(self, message: str) -> str:
        return input(message)

    def flush(self):
        raise NotImplementedError



class Game:

    def __init__(self, player: Party):
        self._player: Party = player
        self._output_stream: BaseInterface = None

    def start(self, output_stream: BaseInterface):
        self._output_stream = output_stream
        self._search_for_dungeon()
        self._explore_dungeon()

    def get_output(self):
        return self._output_stream


    def rest_continue(self) -> bool:
        if not self._player.has_movement():
            self._player.rest()
            self._output_stream.write("Completely Exhausted, you are forced to rest")
            self._output_stream.write(f"MP replenished. Total MP: {self._player.move_point}")
            # ToDo: Figure out why these three lines don't work in both rest blocks
            self._output_stream.write(f"HP replenished. Total HP: {self._player.health}")
            self._output_stream.write(f"-1 Supplies. Total Supplies: {self._player.supplies}")
            return True
        else:
            while True:
                rest_enter = int(input("Enter 1 to rest, 2 to continue exploring, or 3 to leave with your treasure\n"))
                if PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.REST:
                    self._player.rest()
                    self._output_stream.write(f"MP replenished. Total MP: {self._player.move_point}")
                    self._output_stream.write(f"HP replenished. Total HP: {self._player.health}")
                    self._output_stream.write(f"-1 Supplies. Total Supplies: {self._player.supplies}")
                    return True
                elif PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.CONTINUE:
                    return True
                elif PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.LEAVE:
                    return False
                elif PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.UNKNOWN:
                    continue

    def _search_for_entrance(self) -> bool:
        dungeon_chance = randint(1, 10)
        if dungeon_chance > 6:
            self._output_stream.write("You have found a dungeon!")
            return True
        elif dungeon_chance > 2 and self._player.expertise is True:  # do the method thing
            self._output_stream.write("Thanks to your expertise,you have found a dungeon!")
            return True
        else:
            return False

    def _search_for_dungeon(self):
        continue_exploration = True
        dungeon_found = False
        while continue_exploration and not dungeon_found and self._player.has_supplies():
            self._player.spend_mp()
            self._output_stream.write("Searching for a dungeon")
            self._output_stream.write("-1 MP")
            self._output_stream.write(f"You have {self._player.move_point} MP remaining")
            dungeon_found = self._search_for_entrance()
            self._output_stream.write("")
            continue_exploration = rest_continue(self._player)

    def _explore_dungeon(self):
        continue_exploration = True
        while continue_exploration and self._player.is_alive() and self._player.has_supplies():
            room = Room.random()
            self._handle_room(room)
            self._output_stream.write("")
            if not self._player.is_alive():
                self._player.lose_treasure()
                break
            continue_exploration = rest_continue(self._player)

    @staticmethod
    def _get_dungeon_room() -> 'Room':
        return Room.random()

    def _handle_room(self, room: Room):
        self._player.spend_mp()
        self._output_stream.write("You enter a new room in the dungeon")
        self._output_stream.write("-1 MP")
        if room.get_monster() is not None:
            self._handle_combat(room.get_monster())
        if room.loot_value == 900:
            self._output_stream.write("You have found an artifact that looks valuable")
        if room.loot_value == 900 and self._player.expertise is True:
            self._output_stream.write("Given your profession, you know the perfect buyer")
            room.loot_value += 200
        self._player.add_loot(room.loot_value)
        if self._player.is_alive():
            self._output_stream.write("")
            self._output_stream.write(f"You loot {room.loot_value} from the room "
                                      f"for a total value of {self._player.treasure}")
            self._output_stream.write(f"You have {self._player.health} HP remaining")
            self._output_stream.write(f"You have {self._player.move_point} MP remaining")
        else:
            self._output_stream.write("")
            self._output_stream.write(f"You have died and lost all your treasure!")

    def _handle_combat(self, monster: Enemy):
        self._output_stream.write("")
        self._output_stream.write("The undead rise from their tombs and attack!")
        self._output_stream.write("-1 MP")
        self._player.spend_mp()
        while self._player.is_alive() and monster.is_alive():
            self._player.lose_hp(monster.damage)
            self._output_stream.write("")
            self._output_stream.write(f"The undead deal {monster.damage}")
            self._output_stream.write(f"You have {self._player.health} HP remaining")
            if not self._player.is_alive():
                break
            monster.lose_hp(self._player.damage)
            self._output_stream.write("")
            self._output_stream.write(f"The party strikes back for {self._player.damage}")
            self._output_stream.write(f"The undead have {monster.health} HP remaining")
