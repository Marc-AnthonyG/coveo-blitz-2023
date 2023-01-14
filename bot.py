from game_message import *
from game_message import GameMessage, TowerType, BuildAction, Position, SendReinforcementsAction, EnemyType, Tower, PlayArea
from actions import *
import random
from typing import List


class Bot:

    def __init__(self):
        self.isSpkike = True
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        if (self.isSpkike):
            pass

        # all possible positions to place a tower
        possibilePositions = self._get_possible_positions(game_message)

        # best position for each tower
        bestPostionForEachTower = self.get_best_tower(
            possibilePositions, game_message)

        for towerType in bestPostionForEachTower.keys():
            actions.append(BuildAction(
                towerType, bestPostionForEachTower[towerType].position))

        return actions
    # SPIKE_SHOOTER = "SPIKE_SHOOTER"
    # BOMB_SHOOTER = "BOMB_SHOOTER"
    # SPEAR_SHOOTER = "SPEAR_SHOOTER"

    def trouver_rayon_attaque(self, tiles_path: list, position: Position, type_tower: TowerType):
        liste_shoot_x = []
        liste_shoot_y = []
        rayon_attaque = []
        tiles_rayon = []
        liste_loops = [-2, -1, 0, 1, 2]
        if type_tower == "SPEAR_SHOOTER" or type_tower == "BOMB_SHOOTER":
            liste_loops = [-2, -1, 0, 1, 2]

        elif type_tower == "BOMB_SHOOTER":
            liste_loop = [-1, 0, 1]

        for i in liste_loops:
            if (position.x + i >= 0):
                liste_shoot_x.append(position.x + i)
        for i in liste_loops:
            if (position.x + i >= 0):
                liste_shoot_y.append(position.y + i)
        for position_x in liste_shoot_x:
            for position_y in liste_shoot_y:
                rayon_attaque.append(
                    Position(position_x, position_y))

        for tile in rayon_attaque:
            if tile in tiles_path:
                tiles_rayon.append(tile)

        return tiles_rayon

    def _get_possible_positions(self, game_message: GameMessage):
        # creates a list containing all useable positions to place a tower
        possible_positions = []
        for x in range(GameMessage.map.width):
            for y in range(GameMessage.map.height):
                next_position = Position()
                next_position.x, next_position.y = x, y
                if not game_message.playAreas[game_message.teamId].is_empty(next_position):
                    possible_positions.append(next_position)
        return possible_positions

    def _in_path(self, game_message: GameMessage, position: Position):
        for path in game_message.map.paths:
            for pos in path.tiles:
                if pos.x == position.x and pos.y == position.y:
                    return True
        return False

    def _get_best_tower(self, possiblePosition: List[Position], game_message: GameMessage)):

        # Contient les 3 tours avec tous les rayson d'attaque de ces tours
        rayonAction={}
        bestPositionForEachTower={}

        allPaths=[]
        for path in game_message.map.paths:
            for tile in path.tiles:
                if tile not in allPaths:
                    allPaths.append(path.tiles)


        for position in possiblePosition:
            for towerType in TowerType:
                rayonAction[towerType]=[]
                rayonAction[towerType].append(
                    {'position': position, 'rayonAction': self.trouver_rayon_attaque(allPaths, position, towerType)})
        for towerType in TowerType:
            bestPositionForEachTower[towerType]=evaluate_function(
                rayonAction[towerType].rayonAction)

        return bestPositionForEachTower


def evaluate_function(rayonsDAttaque: list[Position]):
    maxTouchedTile = 0
    bestPosition = Position()
    for rayonAction in rayonsDAttaque:
        if len(rayonAction) > maxTouchedTile:
            maxTouchedTile = len(rayonAction)
            bestPosition = rayonAction.position

    return {'position': bestPosition, 'tileTouched': maxTouchedTile}
