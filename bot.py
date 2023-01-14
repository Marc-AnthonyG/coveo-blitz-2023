from game_message import *
from game_message import GameMessage, TowerType, Position, EnemyType, Tower, PlayArea
from actions import *
import random


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        other_team_ids = [
            team for team in game_message.teams if team != game_message.teamId]
        actions = list()

        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(
            random.randint(1, game_message.map.width), random.randint(1, game_message.map.height))))

        #actions.append(SellAction(Position(0, 0)))
        #actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(0, 0)))

        if other_team_ids:
            actions.append(SendReinforcementsAction(
                EnemyType.LVL1, other_team_ids[0]))

        return actions
    #SPIKE_SHOOTER = "SPIKE_SHOOTER"
    #BOMB_SHOOTER = "BOMB_SHOOTER"
    #SPEAR_SHOOTER = "SPEAR_SHOOTER"

    def trouver_rayon_attaque(self, tiles_path: list, position: Position, type_tower: TowerType):
        liste_shoot_x = []
        liste_shoot_y = []
        rayon_attaque = []
        liste_loops = [-2, -1, 0, 1, 2]
        if type_tower == "SPEAR_SHOOTER":
            for i in liste_loops:
                if (position.x + i >= 0):
                    liste_shoot_x.append(position.x + i)
            for i in liste_loops:
                if (position.x + i >= 0):
                    liste_shoot_y.append(position.y + i)
            for position_x in liste_shoot_x:
                for position_y in liste_shoot_y:
                    liste_position_attaque.append(
                        Position(position_x, position_y))

            for tile in rayon_attaque:

            liste_shoot_x.append(position.x - 2)
            coin_sup_droit_y = position.y + 2

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
                next_position = Position()
                next_position.x, next_position.y = x, y
                if not game_message.playAreas[game_message.teamId].get_tile_at(next_position).hasObstacle:
                    possible_positions.append(next_position)
        return possible_positions

    def _get_best_tower(self, possiblePosition: List[Position]):

        # Contient les 3 tours avec tous les rayson d'attaque de ces tours
        rayonAction = {}
        bestPositionForEachTower = {}

        for position in possiblePosition:
            for towerType in TowerType:
                for

                # 'position': position, 'rayonAction': self.trouver_rayon_attaque(position, towerType)}


def evaluate_function(rayonsDAttaque: list[Position]):
    best
