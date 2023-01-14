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
            # actions.append(buy)
            pass

        # all possible positions to place a tower
        possibilePositions = self._get_possible_positions(game_message)

        # best position for each tower
        bestPostionForEachTower = self._get_positions(game_message,
                                                      possibilePositions)

        for towerType in bestPostionForEachTower.keys():
            if bestPostionForEachTower[towerType] != False:
                actions.append(BuildAction(
                    towerType, bestPostionForEachTower[towerType]))

                index = self._index_of(
                    possibilePositions, bestPostionForEachTower[towerType])
                del possibilePositions[index]
                bestPostionForEachTower = self._get_positions(
                    game_message, possibilePositions)

        if (game_message.teamInfos[game_message.teamId].money > 2000):
            positionReplaceArcherToBomber = self.replace_archer_to_bomber(
                game_message)
            actions.append(SellAction(positionReplaceArcherToBomber))
            actions.append(BuildAction(TowerType.BOMB_SHOOTER,
                           positionReplaceArcherToBomber))

        return actions

    def trouver_tuiles_touchees(self, tiles_path: list, position: Position, type_tower: TowerType):
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

    def _get_best_tower(self, possiblePositions: List[Position], game_message: GameMessage):

        # Contient les 3 tours avec tous les rayson d'attaque de ces tours
        listeTilesTouchees = {}
        bestPositionForEachTower = {}

        towerTypesEnum = [TowerType.BOMB_SHOOTER,
                          TowerType.SPEAR_SHOOTER, TowerType.SPIKE_SHOOTER]

        allPaths = []
        # getting all path tiles and making sure they are not already in
        for path in game_message.map.paths:
            for tile in path.tiles:
                if not self._is_in(allPaths, tile):
                    allPaths.append(tile)

        # calculating a list of every touched tile for every single possible tile
        for positionLibre in possiblePositions:
            for towerType in towerTypesEnum:
                listeTilesTouchees[towerType] = []
                rayon = self.trouver_tuiles_touchees(
                    allPaths, positionLibre, towerType)
                listeTilesTouchees[towerType].append(
                    {'position': positionLibre, 'rayonAction': rayon})
        # for each tower type, finding out which tile is the best one to place it on
        for towerType in towerTypesEnum:
            positions = []
            for element in listeTilesTouchees[towerType]:
                if element['rayonAction'] != []:
                    positions.append(element["rayonAction"])

        return bestPositionForEachTower

    def _get_positions(self, game_message, possible_positions):
        listeTilesTouchees = {}
        listeTuilesPossibles = {}
        towerTypesEnum = [TowerType.BOMB_SHOOTER,
                          TowerType.SPEAR_SHOOTER, TowerType.SPIKE_SHOOTER]

        # getting all path tiles and making sure they are not already in
        all_paths = []
        for path in game_message.map.paths:
            for tile in path.tiles:
                if not self._is_in(all_paths, tile):
                    all_paths.append(tile)

        available_tower_types = []
        for type in towerTypesEnum:
            if game_message.teamInfos[game_message.teamId].money < game_message.shop.towers[type].price:
                continue
            available_tower_types.append(type)
            listeTilesTouchees[type] = []
            listeTuilesPossibles[type] = []
            for position in possible_positions:

                tuiles_touchees = self.trouver_tuiles_touchees(
                    all_paths, position, type)
                if tuiles_touchees:
                    listeTilesTouchees[type].append(
                        {'position': position, 'rayonAction': tuiles_touchees})
                    listeTuilesPossibles[type].append(position)

        answer = {}
        for type in available_tower_types:
            answer[type] = self._get_max_of(
                listeTilesTouchees[type], listeTuilesPossibles[type])
        return answer

    def look_to_buy(self, game_message: GameMessage):
        if len(game_message.playAreas[game_message.teamId].towers)*5 > game_message.round:
            itemToSell = sorted(
                game_message.shop.reinforcements.keys(), key=lambda x: x.upper())

            for item in itemToSell:
                if game_message.teamInfos[game_message.teamId].money >= game_message.shop.reinforcements[item].price*8:
                    other_team_ids = [
                        team for team in game_message.teams if team != game_message.teamId]
                    return SendReinforcementsAction(item, other_team_ids[0])
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
        for tower in game_message.playAreas[game_message.teamId].towers:
            if tower.type == TowerType.SPEAR_SHOOTER:
                return tower.position
        return None

    def _get_max_of(self, all_touched_of_type, positions):
        best_position = positions[0]
        max_touched = 0

        for i in range(len(positions)):  # toutes les positions ou on peut placer de quoi
            # si ca touche beaucoup de case
            if len(all_touched_of_type[i]) > max_touched:
                best_position = positions[i]
                max_touched = len(all_touched_of_type[i])

        print(max_touched)

        return best_position
