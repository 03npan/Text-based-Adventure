import world
from player import Player

def get_player_command():
    return input("Action: ")

def play():
    #UNUSED CODE, KEPT FOR REFERENCE
    #world.load_tiles()
    print("Example text adventure. Credits to Phillip Johnson")
    player = Player()
    #UNUSED CODE, KEPT FOR REFERENCE
    #room = world.tile_exists(player.location_x, player.location_y)
    room = world.tile_at(player.x, player.y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        #UNUSED CODE, KEPT FOR REFERENCE
        #room = world.tile_exists(player.location_x, player.location_y)
        room = world.tile_at(player.x, player.y)
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            print("Choose an action:\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            action_input = get_player_command()
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break

if __name__ == "__main__":
    play()