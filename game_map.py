import numpy as np  # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    # GameMap is a class that represents a map of the game world.  It is a 2D array of tiles.
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        self.tiles[30:33, 22] = tile_types.wall

    # in_bounds is a method that returns True if the given x and y coordinates are within the bounds of the map.
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    # render is a method that draws the map to the console.
    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]