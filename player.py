import sys
import random
from abc import abstractmethod
from util import *
from piece import *



TARGET_CORNERS_MAP = {
    0: (4, 16),
    1: (0, 12),
    2: (4, 4),
    3: (12, 0),
    4: (16, 4),
    5: (12, 12)
}

class Player:
    def __init__(self, player_id, initial_places, final_places):
        self.player_id = player_id
        self.color = COLOR_MAP[self.player_id]
        self.pieces = [None] * len(initial_places)
        for i, _ in enumerate(self.pieces):
            self.pieces[i] = Piece(self.player_id)

        self.has_won = False
        self.initial_places = initial_places
        self.final_places = final_places
        self.target_corner = TARGET_CORNERS_MAP[self.player_id] 
    
    # whether board_state is goal state for this player
    def is_goal_state(self, board_state):
        for place in self.final_places:
            if board_state[place] not in self.pieces:
                return False
        return True
    
    # return total distance of all pieces to target corner
    def evaluate(self, board_state):
        total_distance = 0
        for pos, occupant in board_state.items():
            if occupant is not None and occupant.player_id == self.player_id:
                piece_distance = hex_distance(pos, self.target_corner)
                # print("distance from ", pos, " to ", self.target_corner, " is ", piece_distance)
                total_distance += piece_distance

        return total_distance
    
    # screen and players are used when loop is needed to wait for input
    @abstractmethod
    def make_move(self, board_state, screen=None):
        pass
    
            


class Human(Player):
    def __init__(self, player_id, initial_positions, final_positions):
        super().__init__(player_id, initial_positions, final_positions)

    def make_move(self, board_state, screen):

        mouse = None
        piece_selected_at = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BOARD_COLOR)
            draw_board_state(screen, board_state)

            prev_mouse = mouse
            mouse = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

            mouse_x, mouse_y = mouse[0]
            left_button_down = mouse[1][0]
            prev_left_button_down = prev_mouse[1][0] if prev_mouse else None

            if piece_selected_at:
                for pos in board_state: # just for iteration, also checked by legal_moves
                    if math.sqrt((mouse_x - axial_to_pixel(pos[0], pos[1], F)[0])**2 + (mouse_y - axial_to_pixel(pos[0], pos[1], F)[1])**2) < PLACE_RAD:
                        draw_transparent_circle(screen, list(board_state[piece_selected_at].color), axial_to_pixel(pos[0], pos[1], 20), PLACE_RAD, 128)  # 128 for 50% transparency
                        if prev_left_button_down and not left_button_down:
                            if pos in get_legal_moves(piece_selected_at, board_state):
                                move_piece(piece_selected_at, pos, board_state)
                                piece_selected_at = None
                                prev_left_button_down = False # hack
                                return

            piece_highlighted_at = None
            for pos in board_state:
                if board_state[pos] is not None and board_state[pos].player_id == self.player_id:
                    if math.sqrt((mouse_x - axial_to_pixel(pos[0], pos[1], F)[0])**2 + (mouse_y - axial_to_pixel(pos[0], pos[1], F)[1])**2) < PLACE_RAD:
                        piece_highlighted_at = pos
                        if prev_left_button_down and not left_button_down:
                            piece_selected_at = piece_highlighted_at
                    if piece_highlighted_at == pos or piece_selected_at == pos:
                        if piece_highlighted_at:
                            pygame.draw.circle(screen, board_state[piece_highlighted_at].color, axial_to_pixel(piece_highlighted_at[0], piece_highlighted_at[1], 20), radius=PLACE_RAD + 3)
                        if piece_selected_at:
                            pygame.draw.circle(screen, board_state[piece_selected_at].color, axial_to_pixel(piece_selected_at[0], piece_selected_at[1], 20), radius=PLACE_RAD + 5)
        
            pygame.display.update()



class Agent(Player):
    def __init__(self, player_id, initial_positions, final_positions, manual):
        super().__init__(player_id, initial_positions, final_positions)
        self.manual = manual

    def make_move(self, board_state, screen=None):
        if not self.manual: # if not manual, agent makes move
            move = self.get_move(board_state)
            move_piece(move[0], move[1], board_state)
            # print(f'Move made: {move[0]} -> {move[1]}')
            # print(f'Board state at {move[1]}: {board_state[move[1]]}')
        else: # otherwise wait for click
            mouse = None
            flag = True

            print(f'Click to make move for player {self.player_id}')

            while flag:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                prev_mouse = mouse
                mouse = [pygame.mouse.get_pos(), pygame.mouse.get_pressed()]
                left_button_down = mouse[1][0]
                prev_left_button_down = prev_mouse[1][0] if prev_mouse else None

                if prev_left_button_down and not left_button_down:
                    move = self.get_move(board_state)
                    move_piece(move[0], move[1], board_state)
                    flag = False

                screen.fill(BOARD_COLOR)
                draw_board_state(screen, board_state)
                pygame.display.update()

    @abstractmethod
    def get_move(self, board_state):
        pass
    


class Random_Agent(Agent):
    def __init__(self, player_id, initial_positions, final_positions, manual):
        super().__init__(player_id, initial_positions, final_positions, manual)
    
    def get_move(self, board_state):
        move = None # tuple of two axial coordinates, e.g. move = ((0, 0), (1, 0))

        legal_moves = [] # list of tuples of two sets of axial coordinates, e.g. legal_moves = [((0, 0), (1, 0)), ((0, 0), (0, 1))]
        for pos in board_state:
            if board_state[pos] is not None and board_state[pos].player_id == self.player_id:
                legal_moves += [(pos, legal_move) for legal_move in get_legal_moves(pos, board_state)]

        # pick a random legal move
        if legal_moves:
            move = random.choice(legal_moves)
        else:
            print("No legal moves")

        # print(f"Total distance to {self.target_corner}: {self.evaluate(board_state)} before move")
        return move
    
# Greedy agent that picks the move that minimizes the total hex distance of all pieces to the target corner. If multiple moves have the same score, it picks one randomly.
class Greedy_Agent(Agent):
    def __init__(self, player_id, initial_positions, final_positions, manual):
        super().__init__(player_id, initial_positions, final_positions, manual)
    
    def get_move(self, board_state):
        best_move = None
        best_score = float('inf')
        for pos in board_state:
            if board_state[pos] is not None and board_state[pos].player_id == self.player_id:
                legal_moves = [(pos, legal_move) for legal_move in get_legal_moves(pos, board_state)]
                for move in legal_moves:
                    next_state = apply_move(move, board_state)
                    score = self.evaluate(next_state)
                    if score < best_score:
                        best_score = score
                        best_move = move
                    elif score == best_score:
                        if random.choice([True, False]):
                            best_score = score
                            best_move = move
        
        return best_move

    

# class DFS_Agent(Agent):
#     def __init__(self, player_id, MANUAL = False):
#         super().__init__(player_id, MANUAL)
    
#     def get_move(self, board_state):
#         # Initial call to the recursive DFS function
#         best_move, _ = self.dfs(board_state, 0, 5)  # Example: max_depth is 5
#         return best_move
    
#     def dfs(self, board_state, depth, max_depth):
#         if depth == max_depth or self.is_goal_state(board_state):
#             return None, self.evaluate(board_state)
        
#         best_score = float('inf')  # Set to infinity because we are minimizing
#         best_move = None
#         for pos in board_state:
#             if board_state[pos] == self.player_id:
#                 legal_moves = get_legal_moves(pos, board_state)
#                 for move in legal_moves:
#                     next_state = self.apply_move(board_state, move)
#                     _, score = self.dfs(next_state, depth + 1, max_depth)
#                     if score < best_score:  # Update to find minimum score
#                         best_score = score
#                         best_move = move
        
#         return best_move, best_score

        
