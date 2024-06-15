import sys
import math
import pygame

# Constants
F = 20
PLACE_LABELS = False
WIDTH, HEIGHT = 800, 600
BOARD_COLOR = (180, 160, 120)
PLACE_RAD = 8
COLOR_MAP = {
    0: (0, 230, 0), 
    1: (0, 0, 0),
    2: (230, 230, 230),
    3: (0, 0, 230), 
    4: (230, 0, 0),
    5: (230, 230, 0)
}

BOARD_SHAPE = ((
    (12, 0),
    (11, 1), (12, 1),
    (10, 2), (11, 2), (12, 2),
    (9, 3), (10, 3), (11, 3), (12, 3),
    (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4),
    (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5),
    (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6),
    (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7),
    (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8),
    (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9), (12, 9),
    (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10),
    (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (11, 11), (12, 11),
    (0, 12), (1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12),
    (4, 13), (5, 13), (6, 13), (7, 13),
    (4, 14), (5, 14), (6, 14),
    (4, 15), (5, 15),
    (4, 16)
))
INITIAL_POSITIONS_MAP = {
    0: [(12, 0), (11, 1), (12, 1), (10, 2), (11, 2), (12, 2), (9, 3), (10, 3), (11, 3), (12, 3)],
    1: [(13, 4), (14, 4), (15, 4), (16, 4), (13, 5), (14, 5), (15, 5), (13, 6), (14, 6), (13, 7)],
    2: [(12, 9), (11, 10), (12, 10), (10, 11), (11, 11), (12, 11), (9, 12), (10, 12), (11, 12), (12, 12)],
    3: [(4, 13), (5, 13), (6, 13), (7, 13), (4, 14), (5, 14), (6, 14), (4, 15), (5, 15), (4, 16)],
    4: [(0, 12), (1, 12), (2, 12), (3, 12), (1, 11), (2, 11), (3, 11), (2, 10), (3, 10), (3, 9)],
    5: [(4, 7), (4, 6), (5, 6), (4, 5), (5, 5), (6, 5), (4, 4), (5, 4), (6, 4), (7, 4)]
}
FINAL_POSITIONS_MAP = {
    0: [(4, 13), (5, 13), (6, 13), (7, 13), (4, 14), (5, 14), (6, 14), (4, 15), (5, 15), (4, 16)],
    1: [(0, 12), (1, 12), (2, 12), (3, 12), (1, 11), (2, 11), (3, 11), (2, 10), (3, 10), (3, 9)],
    2: [(4, 7), (4, 6), (5, 6), (4, 5), (5, 5), (6, 5), (4, 4), (5, 4), (6, 4), (7, 4)],
    3: [(12, 0), (11, 1), (12, 1), (10, 2), (11, 2), (12, 2), (9, 3), (10, 3), (11, 3), (12, 3)],
    4: [(13, 4), (14, 4), (15, 4), (16, 4), (13, 5), (14, 5), (15, 5), (13, 6), (14, 6), (13, 7)],
    5: [(12, 9), (11, 10), (12, 10), (10, 11), (11, 11), (12, 11), (9, 12), (10, 12), (11, 12), (12, 12)]
}

# utility functions

# returns a new board state after applying a move without updating board state
def apply_move(move, board_state):
    new_board_state = board_state.copy()
    update_board_state(move, new_board_state)
    return new_board_state

# modifies board_state, no return value
def update_board_state(move, board_state):
    board_state[move[1]] = board_state[move[0]]
    board_state[move[0]] = None

# initializes board state
def initialize_board_state(board_shape, players):
    board_state = {place: None for place in board_shape}
    for player in players:
        for i, place in enumerate(player.initial_places):
            board_state[place] = player.pieces[i]

    return board_state

# takes a position and a board state and returns a list of legal new positions for piece
def get_legal_moves(pos, board_state):
    legal_moves = []
    jump_moves = find_jumps(pos, board_state, pos, [])

    for pos in rad_one(pos):
        if pos in board_state.keys() and board_state[pos] is None:  # pos on board and no piece there
            legal_moves.append(pos)

    legal_moves += jump_moves
    return legal_moves

# recursive helper for get_legal_moves
def find_jumps(start_pos, board_state, current_pos, visited):
    jumps = []

    for pos in rad_one(current_pos):
        if pos in board_state.keys() and board_state[pos] is not None:  # pos on board and piece there to jump over
            new_pos = over(current_pos, pos)
            if new_pos in board_state.keys() and board_state[new_pos] is None and new_pos not in visited:
                jumps.append(new_pos)
                visited.append(new_pos)
                jumps += find_jumps(start_pos, board_state, new_pos, visited)
    
    return jumps

# moves a piece
def move_piece(piece_pos, new_pos, board_state):
    if new_pos in get_legal_moves(piece_pos, board_state):
        update_board_state((piece_pos, new_pos), board_state)

# geometric helpers

# takes pos and position of piece to jump over and returns new position after jump
def over(pos, jump_over):
    q, r = pos
    q2, r2 = jump_over
    return (2*q2 - q, 2*r2 - r)

# returns a list of positions one radius away from a given position
def rad_one(pos):
    q, r = pos
    return [(q, r-1), (q+1, r-1), (q+1, r), (q, r+1), (q-1, r+1), (q-1, r)]

# returns the integer axial distance between two places
def hex_distance(pos1, pos2):
    q1, r1 = pos1
    q2, r2 = pos2
    return max(abs(q1 - q2), abs(r1 - r2), abs(q1 + r1 - q2 - r2))

# converts axial coordinates to pixel coordinates
def axial_to_pixel(q, r, f):
    x = f * math.sqrt(3) * (q + r / 2)
    y = f * (3 / 2) * r
    return x, y



# drawing helpers

def draw_transparent_circle(screen, color, pos, radius, alpha):
    circle_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    circle_color = color + [alpha,]  # Adding the alpha value to the color tuple
    pygame.draw.circle(circle_surface, circle_color, (radius, radius), radius)
    screen.blit(circle_surface, (pos[0] - radius, pos[1] - radius))

def draw_polygon(surface, color, points):
    pixel_points = []
    for point in points:
        pixel_points.append(axial_to_pixel(point[0], point[1], 20))
    pygame.draw.polygon(surface, color, pixel_points)

def draw_board_state(surface, board_state):
    draw_polygon(surface, (0, 180, 0), [(12, 0), (8, 4), (12, 4)])
    draw_polygon(surface, (180, 0, 0), [(0, 12), (4, 8), (4, 12)])
    draw_polygon(surface, (0, 0, 180), [(4, 12), (4, 16), (8, 12)])
    draw_polygon(surface, (180, 180, 0), [(8, 4), (4, 4), (4, 8)])
    draw_polygon(surface, (40, 40, 30), [(12, 4), (16, 4), (12, 8)])
    draw_polygon(surface, (180, 180, 180), [(12, 8), (12, 12), (8, 12)])

    for i in range(0, 17):
        for j in range(0, 17):
            if (i, j) in board_state.keys():
                pygame.draw.circle(surface, (160, 140, 100), axial_to_pixel(i, j, 20), radius=PLACE_RAD)
                if PLACE_LABELS:
                    text = str(i) + ", " + str(j)
                    font = pygame.font.Font(None, 12)
                    text = font.render(text, 1, (255, 255, 255))
                    surface.blit(text, axial_to_pixel(i + .1, j + .2, 20))
    
    for pos in board_state.keys():
        if board_state[pos] is not None:
            pygame.draw.circle(surface, COLOR_MAP[board_state[pos].player_id], axial_to_pixel(pos[0], pos[1], 20), radius=PLACE_RAD)
