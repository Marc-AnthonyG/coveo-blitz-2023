from game_message import *
from game_message import GameMessage, TowerType, Position, EnemyType, Tower, PlayArea
from actions import *
import random
from typing import List


class Bot:

    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []
        
        buy = self.look_to_buy(game_message)
        if buy != False:
            #actions.append(buy)
            pass
        
        print("1")
        # all possible positions to place a tower
        possibilePositions = self._get_possible_positions(game_message)
        print("2")
        # best position for each tower
        bestPostionForEachTower = self._get_best_tower(
            possibilePositions, game_message)
        print("3")
        for towerType in bestPostionForEachTower.keys():
            if bestPostionForEachTower[towerType] != False:
                actions.append(BuildAction(
                    towerType, bestPostionForEachTower[towerType]['position']))
                index = self._index_of(possibilePositions,bestPostionForEachTower[towerType]['position'])
                print(index)
                del possibilePositions[index]
        print(4)
        
        if(game_message.teamInfos[game_message.teamId].money>2000):
            replaceArcherToBomber = self._replace_archer_to_bomber(game_message)
        
    
        return actions


    def trouver_rayon_attaque(self, tiles_path: list, position: Position, type_tower: TowerType):
        liste_shoot_x = []
        liste_shoot_y = []
        rayon_attaque = []
        tiles_rayon = []
        if type_tower == TowerType.SPEAR_SHOOTER or type_tower == TowerType.BOMB_SHOOTER:
            liste_loops = [-2, -1, 0, 1, 2]

        elif type_tower == TowerType.SPIKE_SHOOTER:
            liste_loops = [-1, 0, 1]

        for i in liste_loops:
            if (position.x + i >= 0):
                liste_shoot_x.append(position.x + i)
            if (position.y + i >= 0):
                liste_shoot_y.append(position.y + i)
        for position_x in liste_shoot_x:
            for position_y in liste_shoot_y:
                rayon_attaque.append(
                    Position(position_x, position_y))

        for tile in rayon_attaque:
            if self._is_in(tiles_path, tile):
                # On veut les positions
                tiles_rayon.append(tile)




        return tiles_rayon

    def _get_possible_positions(self, game_message: GameMessage):
        # creates a list containing all useable positions to place a tower
        possible_positions = []
        for x in range(game_message.map.width):
            for y in range(game_message.map.height):
                next_position = Position(x, y)
                if game_message.playAreas[game_message.teamId].is_empty(next_position):
                    possible_positions.append(next_position)
        return possible_positions

    def _in_path(self, game_message: GameMessage, position: Position):
        for path in game_message.map.paths:
            for pos in path.tiles:
                if pos.x == position.x and pos.y == position.y:
                    return True
        return False

    def _get_best_tower(self, possiblePosition: List[Position], game_message: GameMessage):

        # Contient les 3 tours avec tous les rayson d'attaque de ces tours
        rayonAction={}
        bestPositionForEachTower={}

        towerTypesEnum = [TowerType.BOMB_SHOOTER, TowerType.SPEAR_SHOOTER, TowerType.SPIKE_SHOOTER]

        allPaths = []
        for path in game_message.map.paths:
            for tile in path.tiles:
                if not self._is_in(allPaths, tile):
                    allPaths.append(tile)


        for position in possiblePosition:
            for towerType in towerTypesEnum:
                rayonAction[towerType]=[]
                rayon = self.trouver_rayon_attaque(allPaths, position, towerType)
                rayonAction[towerType].append(
                    {'position': position, 'rayonAction': rayon})
        print(rayonAction)
        for towerType in towerTypesEnum:
            
            positions = []
            for element in rayonAction[towerType]:
                if element['rayonAction'] == []:
                    positions.append(element["rayonAction"])
                        
                bestPositionForEachTower[towerType]=evaluate_function(positions)
                print(positions)

        return bestPositionForEachTower
    
    def look_to_buy(self, game_message: GameMessage):
        if len(game_message.playAreas[game_message.teamId].towers)*5>game_message.round:
            itemToSell = sorted(game_message.shop.reinforcements.keys(), key=lambda x:x.upper())
            
            for item in itemToSell:
                print(item)
                if game_message.teamInfos[game_message.teamId].money >= item.price*8:
                    other_team_ids = [team for team in game_message.teams if team != game_message.teamId]
                    return SendReinforcementsAction(item.key, other_team_ids[0])
        return None
    
    def _is_in(self, liste, position):
        for pos in liste:
            if pos.x == position.x and pos.y == position.y:
                return True
        return False
    


    def _index_of(self, liste, position):
        # returns index of position in list
        index = 0
        for element in liste:
            if element.x == position.x and element.y == position.y:
                return index
            index += 1
        return -1
    

    def replace_archer_to_bomber(self, game_message):
        return None

    
    


def evaluate_function(rayonsDAttaque):
    maxTouchedTile = 0
    
    bestPosition = Position(0, 0)
    
    for rayonAction in rayonsDAttaque:
        if len(rayonAction) > maxTouchedTile:
            maxTouchedTile = len(rayonAction)
            bestPosition = rayonAction.position

    return {'position': bestPosition, 'tileTouched': maxTouchedTile}