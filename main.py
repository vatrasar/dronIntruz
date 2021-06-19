from GameState import GameState
from Settings import get_properties


def main():
    settings_map=None
    try:
        settings_map=get_properties()
    except Exception as exp:
        print(str(exp))
        return
    t_curr=0
    game_state=GameState(settings_map)
    print(2)



if __name__ == '__main__':
    main()
