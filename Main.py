import numpy as np

# Create a 3x3x3 array
arr = np.array([np.array([
    [[1, 1, 0],
     [1, 0, 0],
     [1, 1, 0]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]
]), np.array([
    [[0, 1, 1],
     [1, 1, 0],
     [0, 1, 0]],

    [[0, 0, 0],
     [0, 1, 0],
     [0, 0, 0]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]
]), np.array([
    [[1, 0, 0],
     [1, 0, 0],
     [1, 1, 0]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]
]), np.array([
    [[1, 1, 0],
     [1, 0, 0],
     [1, 1, 0]],

    [[1, 0, 0],
     [0, 0, 0],
     [0, 0, 0]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]
]), np.array([
    [[1, 0, 0],
     [1, 1, 0],
     [1, 1, 1]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]],

    [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]
])])

def print_grid(grid):
    print()
    for row in grid:
        for value in row:
            print(value, end=" ")
        print()
    print()

def convert_grid_to_array(grid): # This function takes a 3D list and converts it to an array of 1s and 0s, where 1s represent 'X' and 0s represent '.'
    array = np.zeros((3, 3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if grid[i][j][k] == 'X':
                    array[i][j][k] = 1
    return array

def take_inputs(): # This returns all pieces as 3D numpy arrays; returns a list of 5 pieces, where each piece is a 3D numpy array
    pieces = []
    print("Please input your 5 pieces, one piece at a time, and one layer at a time. Once you finish a layer for one of your pieces, you can move on to the next piece by pressing 'q' and then pressing 'Enter'. Each piece is represented by 3 3x3 grids. If one of the grids is empty, just click enter without changing anything.")
    for i in range(5):
        piece = []
        for j in range(3):
            grid = [["." for _ in range(3)] for _ in range(3)]
            print(f"Enter your 3x3 grid for layer {j+1} of piece {i+1} (use 'x' or '.'): ")
            print_grid(grid)
            while True:
                user_input = input("Enter x,y,value and the commas that separate them (or 'q' to quit): ")
                if user_input.lower() == 'q':
                    break

                try:
                    x, y, value = user_input.split(',')
                    x = int(x)
                    y = int(y)
                    value = value.upper()
                    if x not in range(3) or y not in range(3) or value not in ['.', 'X']:
                        print("Invalid input. Try again.")
                        continue

                    # Update the grid
                    grid[y][x] = value #flipped because the first value gives the equivalent of the y value and the second values gives the equivalent of the x value in a 2D array
                    print_grid (grid)
                except ValueError:
                    print("Invalid format. Use x,y,value")

            piece.insert(0, grid)
        pieces.append(normalize_piece(convert_grid_to_array(piece)))
    return np.array(pieces)

def rotate_piece(piece):
    rotations = []

    def add_unique(rot):
        rot = normalize_piece(rot)
        for r in rotations:
            if np.array_equal(rot, r):
                return
        rotations.append(rot)

    def all_rotations_from_top(p):
        for k in range(4):
            add_unique(np.rot90(p, k=k, axes=(1, 2)))  # spin around vertical axis

    # original orientation (top = +z)
    all_rotations_from_top(piece)

    # flip to bottom (top = -z)
    all_rotations_from_top(np.rot90(piece, 2, axes=(0, 2)))

    # bring +x to top
    all_rotations_from_top(np.rot90(piece, -1, axes=(0, 2)))

    # bring -x to top
    all_rotations_from_top(np.rot90(piece, 1, axes=(0, 2)))

    # bring +y to top
    all_rotations_from_top(np.rot90(piece, 1, axes=(0, 1)))

    # bring -y to top
    all_rotations_from_top(np.rot90(piece, -1, axes=(0, 1)))

    return np.array(rotations)

def can_place(cube, piece_blocks, dx, dy, dz):
    for z in range(3):
        for y in range(3):
            for x in range(3):
                if piece_blocks[z, y, x]:
                    cz, cy, cx = z + dz, y + dy, x + dx
                    if cz >= 3 or cy >= 3 or cx >= 3:
                        return False
                    if cube[cz, cy, cx] != 0:
                        return False
    return True

def place_piece(cube, piece_blocks, dx, dy, dz, piece_id):
    for z in range(3):
        for y in range(3):
            for x in range(3):
                if piece_blocks[z, y, x]:
                    cube[z + dz, y + dy, x + dx] = piece_id

def remove_piece(cube, piece_blocks, dx, dy, dz):
    for z in range(3):
        for y in range(3):
            for x in range(3):
                if piece_blocks[z, y, x]:
                    cube[z + dz, y + dy, x + dx] = 0

def canonical_form(cube):
    rotations = rotate_piece(cube)
    return min(rotations, key=lambda x: x.tobytes())

def check_for_duplicate_solutions(solutions, new_solution):
    canon = canonical_form(new_solution)
    for sol in solutions:
        if np.array_equal(sol, canon):
            return False
    solutions.append(canon)
    return True

def normalize_piece(piece):
    coords = np.argwhere(piece != 0)
    if len(coords) == 0:
        return piece.copy()
    
    min_z, min_y, min_x = coords.min(axis=0)

    normalized = np.zeros_like(piece)
    for z, y, x in coords: 
        normalized[z - min_z, y - min_y, x - min_x] = piece[z, y, x]

    return normalized

def solve_cube(all_pieces, cube=None, piece_index=0, solutions=None):
    if cube is None:
        cube = np.zeros((3, 3, 3), dtype=int)
    if solutions is None:
        solutions = []

    if piece_index == len(all_pieces):
        print("Found a solution! checking if duplicate.")
        if check_for_duplicate_solutions(solutions, cube.copy()):
            print("New unique solution found!")
        else: 
            print("Duplicate solution found, not adding.")
        return

    piece = all_pieces[piece_index]

    for orientation in piece:  # each rotation
        for dz in range(3):
            for dy in range(3):
                for dx in range(3):
                    if can_place(cube, orientation, dx, dy, dz):
                        place_piece(cube, orientation, dx, dy, dz, piece_index + 1)
                        solve_cube(all_pieces, cube, piece_index + 1, solutions)
                        remove_piece(cube, orientation, dx, dy, dz)

arr = take_inputs() # This will prompt the user to input their pieces and store them as 3D numpy arrays in a list called arr

all_types = [
    rotate_piece(arr[0]),  # list of rotations of piece1
    rotate_piece(arr[1]),  # list of rotations of piece2
    rotate_piece(arr[2]),
    rotate_piece(arr[3]),
    rotate_piece(arr[4])
]



#print(arr)
#print("rotations of pieces: ")
#print(np.array(rotate_piece(arr[1])))
solutions = []
print("Determining all solutions. Please wait.")
solve_cube(all_types, solutions=solutions)
print("solutions: ", np.array(solutions))

