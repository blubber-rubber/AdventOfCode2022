import time
import re

import numpy as np

start_time = time.time()
'''
Given a face in a net, we can only determine the orientation of the (potentially) neighbouring faces

         _______                        _______                        _______            
        |       |                      |       |                      |       |           
        |  B,v  |                      |  U,^  |                      |  U,<  |           
        |       |                      |       |                      |       |           
 ------- ------- -------        ------- ------- -------        ------- ------- -------    
|       |       |       |      |       |       |       |      |       |       |       |  
|  L,>  |  U,^  |  R,<  |      |  L,^  |  F,^  |  R,^  |      |  B,^  |  L,^  |  F,^  |   
|       |       |       |      |       |       |       |      |       |       |       |   
 ------- ------- -------        ------- ------- -------        ------- ------- -------    
        |       |                      |       |                      |       |           
        |  F,^  |                      |  D,v  |                      |  D,<  |           
        |       |                      |       |                      |       |           
         -------                        -------                        _______    
         
         
         _______                        _______                        _______            
        |       |                      |       |                      |       |           
        |  B,^  |                      |  U,v  |                      |  U,>  |           
        |       |                      |       |                      |       |           
 ------- ------- -------        ------- ------- -------        ------- ------- -------    
|       |       |       |      |       |       |       |      |       |       |       |  
|  R,<  |  D,^  |  L,>  |      |  R,^  |  B,^  |  L,^  |      |  F,^  |  R,^  |  B,^  |   
|       |       |       |      |       |       |       |      |       |       |       |   
 ------- ------- -------        ------- ------- -------        ------- ------- -------    
        |       |                      |       |                      |       |           
        |  F,v  |                      |  D,^  |                      |  D,>  |           
        |       |                      |       |                      |       |           
         -------                        -------                        _______           
'''

ROTATIONS = ['^', '>', 'v', '<']
DIRECTIONS2D = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def rotate_symbol(name):
    """ Function updates a face_name to the next rotation in ROTATIONS"""
    letter, s = name
    r_index = ROTATIONS.index(s)
    return letter, ROTATIONS[(r_index + 1) % 4]


class Stamp:
    """
    This class is supposed to encode the orientation of neighbouring faces of a given face in a net
    """

    def __init__(self, name, right, down, left, up):
        self.name = name
        self.right = right
        self.down = down
        self.left = left
        self.up = up

    def rotate(self):
        """
        Rotates the whole stamp
        """
        self.name = rotate_symbol(self.name)
        self.left = rotate_symbol(self.left)
        self.right = rotate_symbol(self.right)
        self.up = rotate_symbol(self.up)
        self.down = rotate_symbol(self.down)
        self.up, self.right, self.down, self.left = self.left, self.up, self.right, self.down

    def get_neighbours(self):
        """
        Returns the neighbouring faces and their orientation
        """

        return [self.right, self.down, self.left, self.up]


# All relevant stamps
STAMPS = {
    'U': Stamp(('U', '^'), ('R', '<'), ('F', '^'), ('L', '>'), ('B', 'v')),
    'D': Stamp(('D', '^'), ('L', '>'), ('F', 'v'), ('R', '<'), ('B', '^')),
    'F': Stamp(('F', '^'), ('R', '^'), ('D', 'v'), ('L', '^'), ('U', '^')),
    'B': Stamp(('B', '^'), ('L', '^'), ('D', '^'), ('R', '^'), ('U', 'v')),
    'L': Stamp(('L', '^'), ('F', '^'), ('D', '<'), ('B', '^'), ('U', '<')),
    'R': Stamp(('R', '^'), ('B', '^'), ('D', '>'), ('F', '^'), ('U', '>')),
}

################# INPUT #####################

with open('input.txt') as f:
    lines = [[x for x in line.rstrip('\n')] for line in f.readlines()]

grid = lines[:-2]
instructions = "".join(lines[-1])

#############################################

n_symbols = sum(sum(x != ' ' for x in line) for line in grid)  # Determine side_length of cube
side_length = int((n_symbols / 6) ** (1 / 2))

squares = []
y = 0
while y * side_length < len(grid):
    x = 0
    while x * side_length < len(grid[y * side_length]):
        if grid[y * side_length][x * side_length] != ' ':
            squares.append((x, y))
        x += 1
    y += 1

squares.sort(key=lambda x: (x[1], x[0]))  # Find top_left mini-square

stamper = [squares[0]]  # positions to be stamped
stamped = set()  # positions already stamped
small_square2face = {squares[0]: ("U", "^")}  # Mini-square to face and orientation

while stamper:  # Still positions to be stamped
    current_pos = stamper.pop(0)
    stamped.add(current_pos)
    current_face, orientation = small_square2face[current_pos]
    stamp = STAMPS[current_face]
    while stamp.name != (current_face, orientation):  # Rotate stamp untill it aligns
        stamp.rotate()

    for index, neighbour_face in enumerate(stamp.get_neighbours()):
        new_pos = (current_pos[0] + DIRECTIONS2D[index][0], current_pos[1] + DIRECTIONS2D[index][1])
        if new_pos in squares and new_pos not in stamped:  # Check if we need to stamp the neighbours
            stamper.append(new_pos)
            small_square2face[new_pos] = neighbour_face


class Face:

    def __init__(self, name, grid, orientation, mini_square):
        self.name = name
        self.grid = grid
        self.og_orientation = orientation
        self.current_orientation = orientation
        self.mini_square = mini_square

    def rotate(self):
        self.name, self.current_orientation = rotate_symbol((self.name, self.current_orientation))
        self.grid = [[self.grid[i][j] for i in range(side_length - 1, -1, -1)] for j in range(side_length)]


FACES = {}
for pos, face in small_square2face.items():
    name, orientation = face
    mini_grid = [[grid[y][x] for x in range(pos[0] * side_length, (pos[0] + 1) * side_length)] for y in
                 range(pos[1] * side_length, (pos[1] + 1) * side_length)]
    FACES[name] = Face(name, mini_grid, orientation, pos)

current_pos = (0, 0)
current_face = FACES["U"]
d_index = 0

start_index = 0
end_index = 0
while end_index < len(instructions):
    while end_index < len(instructions) and not instructions[end_index] in 'LR':
        end_index += 1
    length_instr = int(instructions[start_index:end_index])
    rotation_instr = None if end_index >= len(instructions) else instructions[end_index]

    moving = True
    move_index = 0
    while move_index < length_instr and moving:
        direction = DIRECTIONS2D[d_index]
        new_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
        if 0 <= new_pos[0] < side_length and 0 <= new_pos[1] < side_length:
            if current_face.grid[new_pos[1]][new_pos[0]] != '#':
                current_pos = new_pos
            else:
                moving = False
        else:
            current_face_name = current_face.name
            current_stamp = STAMPS[current_face_name]
            while current_stamp.name != (current_face_name, current_face.current_orientation):
                current_stamp.rotate()
            neighbouring_faces = current_stamp.get_neighbours()
            relevant_neighbour = neighbouring_faces[d_index]
            neighbour_face = FACES[relevant_neighbour[0]]
            while neighbour_face.current_orientation != relevant_neighbour[1]:
                neighbour_face.rotate()
            new_pos = (new_pos[0] % side_length, new_pos[1] % side_length)
            if neighbour_face.grid[new_pos[1]][new_pos[0]] != "#":
                current_pos = new_pos
                current_face = neighbour_face
            else:
                moving = False

        move_index += 1

    if rotation_instr:
        d_index = (d_index + 2 * (rotation_instr == "R") - 1) % len(DIRECTIONS2D)

    end_index += 1
    start_index = end_index


def position_after_rotation(pos):
    # Calculates new coordinates when the current face is rotated
    return side_length - 1 - pos[1], pos[0]


while current_face.current_orientation != current_face.og_orientation:
    current_face.rotate()
    current_pos = position_after_rotation(current_pos)
    d_index = (d_index + 1) % len(DIRECTIONS2D)

left_most = (current_face.mini_square[0] * side_length, current_face.mini_square[1] * side_length)

final_pos = (current_pos[0] + left_most[0], current_pos[1] + left_most[1])

print((final_pos[1] + 1) * 1000 + (final_pos[0] + 1) * 4 + d_index)

print(time.time() - start_time)
