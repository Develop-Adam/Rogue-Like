import tcod

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler

def main():
    # set screen size
    screen_width = 80
    screen_height = 50
    
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
            root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color)
            context.present(root_console)

            # clear the console before the next frame is drawn
            root_console.clear()

            # wait for user input
            for event in tcod.event.wait():
                
                # pass event to event handler
                action = event_handler.dispatch(event)

                # if event handler returns an action, execute it
                if action is None:
                    continue

                # if action is an instance of MovementAction, update player position
                if isinstance(action, MovementAction):
                    player.move(dx=action.dx, dy=action.dy)

                # if action is an instance of EscapeAction, exit the game
                elif isinstance(action, EscapeAction):
                    raise SystemExit()
                

if __name__ == "__main__":
    main()