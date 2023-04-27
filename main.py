from event_handlers import search_for_dungeon, explore_dungeon
from character import Party, Profession
from choice_handlers import party_selector
# TODO: Handle Printing

if __name__ == "__main__":
    profession: Profession = party_selector()
    player_party: Party = Party(profession)
    search_for_dungeon(player_party)
    explore_dungeon(player_party)
    print(f"Your Score: {player_party.treasure}")
    print(f"Player_hp: {player_party.health}")



# class A:
#     def __init__(self, a, b, c, d):
#         self._a = a
#         self._b = b
#         self._c = c
#         self._d = d
#
#     class Builder:

