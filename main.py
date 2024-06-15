import sys
import pygame
from player import *
from util import *

# initialize players
players = [Greedy_Agent(1, INITIAL_POSITIONS_MAP[1], FINAL_POSITIONS_MAP[1], True), Greedy_Agent(4, INITIAL_POSITIONS_MAP[4], FINAL_POSITIONS_MAP[4], True)]

# initialize board_state: keys are all places on board and values are piece on that place, None if empty
board_state = initialize_board_state(BOARD_SHAPE, players)

# initialize Pygame and setup display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chinese Checkers")



def main():
    turn_player = players[0]
    move_counter = 0

    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BOARD_COLOR)
        draw_board_state(screen, board_state)

        if not turn_player.has_won:
            print('Player', turn_player.player_id, 'turn')
            turn_player.make_move(board_state, screen=screen)
            if turn_player.is_goal_state(board_state):
                print('player', turn_player.player_id, 'has won')
                turn_player.has_won = True
        turn_player = players[(players.index(turn_player) + 1) % len(players)]
        move_counter += 1

        pygame.display.update()



if __name__ == "__main__":
    main()
