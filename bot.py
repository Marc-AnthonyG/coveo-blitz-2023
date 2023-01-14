from game_message import *
from game_message import GameMessage, TowerType, Position, EnemyType, Tower, PlayArea
from actions import *
import random
from typing import List


class Bot:

    def __init__(self):
        self.wasSpyke = False
        self.wasSpyke2 = False
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        #if(game_message.ticksUntilPayout != 59):
        #    buy = self.look_to_buy(game_message)
        #    if buy != False:
        #        actions.append(buy)
                

        # all possible positions to place a tower
        possibilePositions = self._get_possible_positions(game_message)

        # best position for each tower
        bestPostionForEachTower = self._get_positions(game_message, possibilePositions)
        
        if(bestPostionForEachTower):
            if(game_message.teamInfos[game_message.teamId].money > 600 and game_message.round > 4):
                actions.append(BuildAction(TowerType.BOMB_SHOOTER, bestPostionForEachTower[TowerType.BOMB_SHOOTER]))
            elif  (game_message.teamInfos[game_message.teamId].money > 280 and game_message.round < 12 and (self.wasSpyke2 == False or game_message.round > 10) ):
                actions.append(BuildAction(TowerType.SPIKE_SHOOTER, bestPostionForEachTower[TowerType.SPIKE_SHOOTER]))
                self.wasSpyke2 = True and self.wasSpyke
                self.wasSpyke = True
            elif  (game_message.teamInfos[game_message.teamId].money > 200 and game_message.round < 10):
                actions.append(BuildAction(TowerType.SPEAR_SHOOTER, bestPostionForEachTower[TowerType.SPEAR_SHOOTER]))
                self.wasSpyke = False
                self.wasSpyke2 = False
        elif (game_message.teamInfos[game_message.teamId].money > 1000):
            positionReplaceArcherToBomber = self.replace_archer_to_bomber(game_message)
            if(positionReplaceArcherToBomber):
                actions.append(SellAction(positionReplaceArcherToBomber))
                actions.append(BuildAction(TowerType.BOMB_SHOOTER, positionReplaceArcherToBomber))
            else:
                positionReplaceSpikerToBomber = self.replace_spiker_to_bomber(game_message)
                if(positionReplaceSpikerToBomber):
                    actions.append(SellAction(positionReplaceSpikerToBomber))
                    actions.append(BuildAction(TowerType.BOMB_SHOOTER, positionReplaceSpikerToBomber))
        

        return actions

    def trouver_tuiles_touchees(self, tiles_path: list, position: Position, type_tower: TowerType, game_message: GameMessage):
        liste_shoot_x = []
        liste_shoot_y = []
        tiles_rayon = 0
        if type_tower == TowerType.SPEAR_SHOOTER or type_tower == TowerType.BOMB_SHOOTER:
            liste_loops = [-2, -1, 0, 1, 2]

        elif type_tower == TowerType.SPIKE_SHOOTER:
            liste_loops = [-1, 0, 1]

        #Vérifie la possibilité 
        for i in liste_loops:
            if (position.x + i >= 0 and position.x + i < game_message.map.width):
                liste_shoot_x.append(position.x + i)
            if (position.y + i >= 0 and position.y + i < game_message.map.height):
                liste_shoot_y.append(position.y + i)


        for position_x in liste_shoot_x:
            for position_y in liste_shoot_y:
                if(self._is_in(tiles_path, Position(position_x, position_y))):
                    tiles_rayon+=1

        return tiles_rayon

    def _get_possible_positions(self, game_message: GameMessage):
        # creates a list containing all useable positions to place a tower
        possible_positions = []

        allPaths = []
        # getting all path tiles and making sure they are not already in
        for path in game_message.map.paths:
            for tile in path.tiles:
                if not self._is_in(allPaths, tile):
                    allPaths.append(tile)

        for x in range(game_message.map.width):
            for y in range(game_message.map.height):
                next_position = Position(x, y)
                if game_message.playAreas[game_message.teamId].is_empty(next_position) and not self._is_in(allPaths, next_position):
                    if game_message.playAreas[game_message.teamId].get_tile_at(next_position) is None:
                        possible_positions.append(next_position)
                    elif not game_message.playAreas[game_message.teamId].get_tile_at(next_position).hasObstacle:
                        possible_positions.append(next_position)
        return possible_positions

    def _in_path(self, game_message: GameMessage, position: Position):
        for path in game_message.map.paths:
            for pos in path.tiles:
                if pos.x == position.x and pos.y == position.y:
                    return True
        return False

    def _get_positions(self, game_message, possible_positions):
        listeTilesTouchees = {}
        listeTuilesPossibles = {}
        towerTypesEnum = [TowerType.BOMB_SHOOTER,
                          TowerType.SPEAR_SHOOTER, TowerType.SPIKE_SHOOTER]

        # getting all path tiles and making sure they are not already in
        all_paths = self._get_all_path(game_message)
        available_tower_types = []


        for type in towerTypesEnum:
            if game_message.teamInfos[game_message.teamId].money < game_message.shop.towers[type].price:
                continue
            available_tower_types.append(type)
            listeTilesTouchees[type] = []
            listeTuilesPossibles[type] = []
            for position in possible_positions:
                tuiles_touchees = self.trouver_tuiles_touchees(all_paths, position, type, game_message)
                if tuiles_touchees:
                    listeTilesTouchees[type].append(tuiles_touchees)
                    listeTuilesPossibles[type].append(position)

        answer = {}

        for type in available_tower_types:
            answer[type] = self._get_max_of(
                listeTilesTouchees[type], listeTuilesPossibles[type], game_message)
        return answer
    
    def _get_all_path(self, game_message: GameMessage):
        all_paths = []
        for path in game_message.map.paths:
            for tile in path.tiles:
                if not self._is_in(all_paths, tile):
                    all_paths.append(tile)
        return all_paths

    def look_to_buy(self, game_message: GameMessage):
        # decide to either buy a tower or attack
        pass

        
        # if len(game_message.playAreas[game_message.teamId].towers) > game_message.round * 2:
        #     itemToSell = sorted(game_message.shop.reinforcements.keys(), key=lambda x: x.upper())

        #     for item in itemToSell:
        #         if game_message.teamInfos[game_message.teamId].money >= game_message.shop.reinforcements[item].price*8:
        #             other_team_ids = [
        #                 team for team in game_message.teams if team != game_message.teamId]
        #             return SendReinforcementsAction(item, other_team_ids[0])
        # return False

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
        for tower in game_message.playAreas[game_message.teamId].towers:
            if tower.type == TowerType.SPEAR_SHOOTER:
                return tower.position
        return None
    
    def replace_spiker_to_bomber(self, game_message):
        for tower in game_message.playAreas[game_message.teamId].towers:
            if tower.type == TowerType.SPIKE_SHOOTER:
                return tower.position
        return None
    


    def _get_max_of(self, all_touched_of_type, positions, game_message):
        best_position = positions[0]
        max_touched = 0


        indexMilieu = int(len(positions) / 2)
        millieuMapHauteur  = int(game_message.map.width / 2)
        millieuMapLargeur  = int(game_message.map.height / 2)


        for i in range(len(positions)):
            if(positions[i].x >= millieuMapLargeur-2 and positions[i].x <= millieuMapLargeur+2 and positions[i].y >= millieuMapHauteur-2 and positions[i].y <= millieuMapHauteur+2):
                if all_touched_of_type[i] > max_touched:
                    best_position = positions[i]
                    max_touched = all_touched_of_type[i]
        
        for i in range(indexMilieu,len(positions)): 
            if all_touched_of_type[i] > max_touched:
                best_position = positions[i]
                max_touched = all_touched_of_type[i]

        for y in range(indexMilieu-1,-1 , -1): 
            if all_touched_of_type[y] > max_touched:
                best_position = positions[y]
                max_touched = all_touched_of_type[y]



        return best_position
