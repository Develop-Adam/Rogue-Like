from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler

# Engine class
class Engine:
    
    # initialize engine with entities, event handler, and player
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
    
    # handle events passed to engine
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
            
            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)
            
            elif isinstance(action, EscapeAction):
                raise SystemExit()
            
    # render entities to console
    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
        
        context.present(console)
        
        console.clear()
