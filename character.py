from enum import Enum


class Profession(Enum):
    UNKNOWN = 0
    MERCENARY = 1
    ARCHEOLOGIST = 2
    MERCHANT = 3

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Entity:
    def __init__(self, health: int, move_point: int, damage: int):
        self.health = health
        self._max_health = health
        self.move_point = move_point
        self._max_move_point = move_point
        self.damage = damage

    def lose_hp(self, damage: int):
        self.health -= damage

    def reset_hp(self):
        self.health = self._max_health

    def is_alive(self) -> bool:
        return self.health > 0


class Enemy(Entity):
    def __init__(self, health: int, damage: int):
        super().__init__(health, 0, damage)


# Make any class variables start with "_" to show it's private and shouldn't be accessed directly
# i.e. player.hp vs player.get_hp()

class Party(Entity):

    def __init__(self, profession: Profession):
        if profession is Profession.MERCENARY:
            self.__internal_init__(10, 150, 15, 10, False, 0)
        elif profession is Profession.ARCHEOLOGIST:
            self.__internal_init__(10, 100, 10, 15, True, 0)
        else:
            self.__internal_init__(15, 100, 10, 10, False, 0)

    def __internal_init__(self, mp: int, hp: int, dam: int, supplies: int, expertise: bool, treasure: int, ):
        self.supplies = supplies
        self.expertise = expertise
        self.treasure = treasure
        super().__init__(hp, mp, dam)

    def add_loot(self, room_loot_value: int):
        self.treasure += room_loot_value

    def lose_treasure(self):
        self.treasure = 0

    def has_movement(self) -> bool:
        return self.move_point > 0

    def rest(self):
        self.move_point = self._max_move_point
        self.supplies -= 1

    def spend_mp(self):
        self.move_point -= 1

    def has_supplies(self) -> bool:
        return self.supplies > 0
