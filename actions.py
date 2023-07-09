# Parent class to all actions in the game. The Action class is a subclass of the built-in object class, and it has no attributes.
class Action:
    pass

# The EscapeAction class is a subclass of Action, and it has no attributes.
class EscapeAction(Action):
    pass

# The MovementAction class is a subclass of Action, and it has two attributes: dx and dy.
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
