import numpy as np
import pygame
import sys
import copy
import time

class Connect4:
    def __init__(self):
        self.ROWS = 6
        self.COLS = 7
        self.board = np.zeros((self.ROWS, self.COLS))
        self.PLAYER = 1
        self.AI = 2
        self.EMPTY = 0

        pygame.init()
        self.SQUARESIZE = 60
        self.width = self.COLS * self.SQUARESIZE
        self.height = (self.ROWS + 1) * self.SQUARESIZE
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect 4")
        self.font = pygame.font.SysFont("monospace", 75)

    def drop_piece(self, board, col, piece):
        for row in range(self.ROWS-1, -1, -1):
            if board[row][col] == self.EMPTY:
                board[row][col] = piece
                return row
        return -1

    def is_valid_move(self, board, col):
        return board[0][col] == self.EMPTY

    def get_valid_moves(self, board):
        return [col for col in range(self.COLS) if self.is_valid_move(board, col)]

    def check_winner(self, board, piece):
        for r in range(self.ROWS):
            for c in range(self.COLS-3):
                if all(board[r][c+i] == piece for i in range(4)):
                    return True

        for r in range(self.ROWS-3):
            for c in range(self.COLS):
                if all(board[r+i][c] == piece for i in range(4)):
                    return True

        for r in range(self.ROWS-3):
            for c in range(self.COLS-3):
                if all(board[r+i][c+i] == piece for i in range(4)):
                    return True
            for c in range(3, self.COLS):
                if all(board[r+i][c-i] == piece for i in range(4)):
                    return True
        return False

    def is_terminal(self, board):
        return self.check_winner(board, self.PLAYER) or self.check_winner(board, self.AI) or len(self.get_valid_moves(board)) == 0

    def evaluate_position(self, board, piece):
       
        score = 0
        opponent = self.PLAYER if piece == self.AI else self.AI

        center_array = [int(i) for i in list(board[:, self.COLS // 2])]
        score += center_array.count(piece) * 3

        for r in range(self.ROWS):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.COLS-3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window, piece, opponent)

        for c in range(self.COLS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.ROWS-3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window, piece, opponent)

        for r in range(self.ROWS-3):
            for c in range(self.COLS-3):
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, piece, opponent)
            for c in range(3, self.COLS):
                window = [board[r+i][c-i] for i in range(4)]
                score += self.evaluate_window(window, piece, opponent)

        return score

    def evaluate_window(self, window, piece, opponent):
        score = 0
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2
        if window.count(opponent) == 3 and window.count(self.EMPTY) == 1:
            score -= 4
        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.is_terminal(board):
            if self.is_terminal(board):
                if self.check_winner(board, self.AI):
                    return None, 1000000
                elif self.check_winner(board, self.PLAYER):
                    return None, -1000000
                else:
                    return None, 0
            return None, self.evaluate_position(board, self.AI)

        valid_moves = self.get_valid_moves(board)
        best_col = valid_moves[0]

        if maximizingPlayer:
            value = float('-inf')
            for col in valid_moves:
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, col, self.AI)
                new_score = self.minimax(board_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:
            value = float('inf')
            for col in valid_moves:
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, col, self.PLAYER)
                new_score = self.minimax(board_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def draw_board(self):

        self.screen.fill((0, 0, 0))

        for c in range(self.COLS):
            for r in range(self.ROWS):
                pygame.draw.rect(self.screen, (0, 0, 255), (c * self.SQUARESIZE, (r+1) * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, (0, 0, 0), (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int((r+1) * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)

        for c in range(self.COLS):
             for r in range(self.ROWS):
                row_index = self.ROWS - 1 - r  # Flip row index for correct drawing

                if self.board[r][c] == self.PLAYER:
                    pygame.draw.circle(self.screen, (255, 0, 0), (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int((row_index + 1) * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                elif self.board[r][c] == self.AI:
                    pygame.draw.circle(self.screen, (255, 255, 0), (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int((row_index + 1) * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)

        pygame.display.update()

    def play_game(self):
      
        game_over = False
        turn = 0
        self.draw_board()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                    col = event.pos[0] // self.SQUARESIZE
                    if self.is_valid_move(self.board, col):
                        self.drop_piece(self.board, col, self.PLAYER)
                        self.draw_board()
                        if self.check_winner(self.board, self.PLAYER):
                            game_over = True
                        turn = 1

            if turn == 1 and not game_over:
                col, _ = self.minimax(self.board, 4, float('-inf'), float('inf'), True)
                self.drop_piece(self.board, col, self.AI)
                self.draw_board()
                if self.check_winner(self.board, self.AI):
                    game_over = True
                turn = 0

if __name__ == "__main__":
    Connect4().play_game()
