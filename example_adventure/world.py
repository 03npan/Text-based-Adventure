import items, enemies, actions, random
from player import Player
#import world

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        #raise NotImplementedError()
        pass

    def adjacent_moves(self):
        #Returns all move actions for adjacent tiles.
        moves = []
        #UNUSED CODE, KEPT FOR REFERENCE
        '''
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        '''
        if tile_at(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if tile_at(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if tile_at(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if tile_at(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
    
    def available_actions(self):
        #Returns all of the available actions in this room.
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.Heal())
        return moves

class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """

    def modify_player(self, player):
        #Room has no action on player
        pass

class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)

class EnemyRoom(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.75:
            self.enemy = enemies.GiantSpider()
            self.alive_text = """
        A giant spider jumps down from its web in front of you!"""
            self.dead_text = """
        The corpse of a dead spider rots on the ground.
        """
        else:
            self.enemy = enemies.Ogre()
            self.alive_text = """
        An ogre is blocking your path!"""
            self.dead_text = """
        A dead ogre reminds you of your triumph."""
        super().__init__(x, y)
    #UNUSED CODE, KEPT FOR REFERENCE
    '''
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
    '''
    #New method
    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

        #UNUSED CODE, KEPT FOR REFERENCE
        '''
        if self.enemy.is_alive():
            return """
        A {} awaits!
            """.format(self.enemy.name)
        else:
            return """
        You've defeated the {}.
            """.format(self.enemy.name)
        '''

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("""
        Enemy does {} damage. You have {} HP remaining.
            """.format(self.enemy.damage, player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            #return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
            return [actions.Flee(tile=self), actions.Attack()]
        else:
            return self.adjacent_moves()# actions.Heal() DOES NOT WORK, MUST CHANGE TO OTHER METHOD OF USER INPUT

class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

#UNUSED CODE, KEPT FOR REFERENCE
'''
class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """
'''
class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())
 
    def intro_text(self):
        return """
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        """

class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!

        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True

world_map = [
    [None, LeaveCaveRoom(1,0),None],
    [None, EnemyRoom(1,1), None],
    [FindDaggerRoom(0,2), StartingRoom(1,2), EnemyRoom(2,2)],
    [None, EmptyCavePath(1,3), None]
]

def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None