from enum import Enum
from character import Profession, Party


class PlayerChoiceEnum(Enum):
    UNKNOWN = 0
    REST = 1
    CONTINUE = 2
    LEAVE = 3

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


def rest_continue(player_party: Party):
    if not player_party.has_movement():
        print("Completely Exhausted, you are forced to rest")
        player_party.rest()
        return True
    else:
        while True:
            rest_enter = int(input("Enter 1 to rest, 2 to continue exploring, or 3 to leave with your treasure\n"))
            if PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.REST:
                player_party.rest()
                return True
            elif PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.CONTINUE:
                return True
            elif PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.LEAVE:
                return False
            elif PlayerChoiceEnum(rest_enter) == PlayerChoiceEnum.UNKNOWN:
                continue


def party_selector() -> Profession:
    print(f"To begin searching for a dungeon choose an adventuring party")
    for profession in Profession:
        if profession is Profession.UNKNOWN:
            continue
        else:
            party = Party(profession)
            print(f' {profession.value}. {profession.name} (MP: {party.move_point} HP : {party.health}, DAM: {party.damage}, '
                  f'Supplies: {party.supplies}, Expertise: {party.expertise})')
    while True:
        selected_value: int = int(input("Enter the number of your party selection\n"))
        if Profession(selected_value) is not Profession.UNKNOWN:
            break
    return Profession(selected_value)
