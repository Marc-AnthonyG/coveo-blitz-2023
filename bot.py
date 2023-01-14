from game_message import *
from actions import *


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
            game_message.map.paths.tiles[6].x+1, game_message.map.paths.tiles[6].y-1)))
        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(
            game_message.map.paths.tiles[15].x+1, game_message.map.paths.tiles[15].y-1)))
        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(17, 20)))

        #actions.append(SellAction(Position(0, 0)))
        #actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(0, 0)))

        if other_team_ids:
            actions.append(SendReinforcementsAction(
                EnemyType.LVL1, other_team_ids[0]))

        return actions
