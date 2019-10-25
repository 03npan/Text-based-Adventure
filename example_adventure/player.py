import random
import items, world
#import world

class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Rock(), items.CrustyBread()]
        self.hp = 100
        #self.location_x, self.location_y = world.starting_position
        self.x = 1
        self.y = 2
        self.victory = False

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')

    def move(self, dx, dy):
        #self.location_x += dx
        #self.location_y += dy
        #print(world.tile_exists(self.location_x, self.location_y).intro_text())
        self.x += dx
        self.y += dy
        print(world.tile_at(self.x, self.y).intro_text())

    def move_north(self):
        self.move(dx=0,dy=-1)

    def move_south(self):
        self.move(dx=0,dy=1)

    def move_east(self):
        self.move(dx=1,dy=0)

    def move_west(self):
        self.move(dx=-1,dy=0)

    #New method, unused
    '''
    def most_powerful_weapon(self, inventory):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
               if item.damage > max_damage:
                   best_weapon = item
                   max_damage = item.damage
            except AttributeError:
                pass            
        return best_weapon

    def attack(self):
        best_weapon = self.most_powerful_weapon(self.inventory)
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print("""
        You use {} against {}!
        """.format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("""
        You killed {}!
            """.format(enemy.name))
        else:
            print("""
        {} HP is {}.
            """.format(enemy.name, enemy.hp))
    '''
    def attack(self):
        best_weapon = None
        max_damage = 0
        for item in self.inventory:
            if isinstance(item, items.Weapon):
                if item.damage > max_damage:
                    max_damage = item.damage
                    best_weapon = item
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print("""
        You use {} against {}!""".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("""
        You killed {}!
            """.format(enemy.name))
        else:
            print("""
        {} HP is {}.""".format(enemy.name, enemy.hp))

    #Consider alternative in the book
    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)
    
    def flee(self, tile):
        #Moves the player randomly to an adjacent tile
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])
    
    #New method
    def heal(self):
        consumables = [item for item in self.inventory if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any items to heal you!")
            return
        for i, item in enumerate(consumables, 1):
            print("Choose an item to use to heal: ")
            print("{}. {}".format(i, item))

            valid = False
            while not valid:
                choice = input("")
                try:
                    to_eat = consumables[int(choice) - 1]
                    self.hp = min(100, self.hp + to_eat.healing_value)
                    self.inventory.remove(to_eat)
                    print("Current HP: {}".format(self.hp))
                    valid = True
                except (ValueError, IndexError):
                    print("Invalid choice, try again.")