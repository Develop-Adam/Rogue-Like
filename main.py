import tcod
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon

def main():
    # set screen size
    screen_width = 80
    screen_height = 50
    
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # set tileset from image in same directory
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # create new event handler
    event_handler = EventHandler()

    # set player position, color, and character
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    # set npc position, color, and character
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    # set list of entities
    entities = {npc, player}

    # generate dungeon
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player,
    )
    
    # create new engine with entities, event handler, and player
    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    # create new terminal with title and vsync enabled.  This is the main window.  The context is the window manager.
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        
        # create a new console with the same dimensions as the main window.  This is the console that will be drawn to.
        root_console = tcod.console.Console(screen_width, screen_height, order="F")

        # main loop
        while True:
            # draw all entities in the list
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()

            # clear the console before the next frame is drawn
            engine.handle_events(events)

                        

if __name__ == "__main__":
    main()