from __future__ import annotations
import random
from typing import Iterator, Tuple, List, TYPE_CHECKING
from game_map import GameMap
import tile_types
import tcod

if TYPE_CHECKING:
    from engine import Entity

class RectagularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        # RectangularRoom is a class that represents a rectangular room on the map.
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        # center is a property that returns the center coordinates of the room.
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        # inner is a property that returns the inner area of the room.
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    # intersects is a method that returns True if this room intersects with another room.
    def intersects(self, other: RectagularRoom) -> bool:
        # return True if this room overlaps with another RectangularRoom
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    # tunnel_between is a function that returns an L-shaped tunnel between two points.
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # move vertically, then horizontally
        corner_x, corner_y = x1, y2
    
    # generate the coordinates for this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectagularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)
        
        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectagularRoom(x, y, room_width, room_height)
        
        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        
        # If there are no intersections then the room is valid.
        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor
        if len(rooms) == 0:
            # The first room, where the player starts.
            player.x, player.y = new_room.center
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
        
        # Finally, append the new room to the list.
        rooms.append(new_room)
    return dungeon