from typing import Optional
import tcod.event
from actions import Action, EscapeAction, MovementAction

# Subclassing tcod.event.EventDispatch allows us to handle events in a more object-oriented way.
class EventHandler(tcod.event.EventDispatch[Action]):

    # This method is called whenever an event is received.
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    # This method is called whenever a key is pressed.
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        # Movement keys
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        # Exit the game
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action