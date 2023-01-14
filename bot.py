from game_message import *
from game_message import GameMessage, TowerType, BuildAction, Position, SendReinforcementsAction, EnemyType, Tower, PlayArea
from actions import *
import random


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        print(game_message.playAreas)

        other_team_ids = [
            team for team in game_message.teams if team != game_message.teamId]
        actions = list()

        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(
            random.randint(1, map.width), random.randint(1, map.height))))

        #actions.append(SellAction(Position(0, 0)))
        #actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(0, 0)))

        if other_team_ids:
            actions.append(SendReinforcementsAction(
                EnemyType.LVL1, other_team_ids[0]))

        return actions
    #SPIKE_SHOOTER = "SPIKE_SHOOTER"
    #BOMB_SHOOTER = "BOMB_SHOOTER"
    #SPEAR_SHOOTER = "SPEAR_SHOOTER"

    def _trouver_rayon_attaque(self, tiles_path: list, position: Position, type_tower: TowerType):
        if type_tower == "SPEAR_SHOOTER":
            pass
        elif type_tower == "BOMB_SHOOTER":
            pass
        else:
            pass
        return

    def _get_possible_positions(self, game_message: GameMessage):
        # creates a list containing all useable positions to place a tower
        possible_positions = []
        for x in range(GameMessage.map.width):
            for y in range(GameMessage.map.height):
                pass
        return


def _get_best_tower(self,):

    rayonAction = []

    for tower in TowerType:
        rayonAction.append(self._trouver_rayon_attaque(tower))
