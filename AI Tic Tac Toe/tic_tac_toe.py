import random

import numpy as np


class TicTacToe:
    def __init__(self) -> None:
        self.board = np.array([" "] * 9).reshape(3, 3)
        self.opponent_move()  # to randomize the board
        self.llm_num_moves = 0

    def observe_board(self) -> str:
        """This tool call is used to observe the board without making a move"""
        row1 = "|".join(self.board[0, :])
        row2 = "|".join(self.board[1, :])
        row3 = "|".join(self.board[2, :])
        bar = "-----"
        return "\n".join([row1, bar, row2, bar, row3])

    def llm_move(self, position: int) -> str:
        """The LLM can put a X on the tic tac toe board using the argument `position` where the value
        is an integer between 1 and 9, inclusive.
        """
        # sanity check
        if not isinstance(position, int) or position not in range(1, 10):
            return f"Invalid move, please try again with the board looking like this:\n{self.observe_board()}"

        # put X on board
        position -= 1
        if self.board[position // 3, position % 3] == " ":
            self.board[position // 3, position % 3] = "X"
            # print(self.board)
            self.llm_num_moves += 1
        else:
            return f"Invalid move, please try again with the board looking like this:\n{self.observe_board()}"

        # check if user wins
        if self.check_if_a_player_won(marker="X"):
            return (
                f"You won! Board looks like this:\n{self.observe_board()}\n"
                f"You have made {self.llm_num_moves} moves"
            )

        # put O on board
        if (self.board == " ").any():
            self.opponent_move()

        # check if opponent wins
        if self.check_if_a_player_won(marker="O"):
            return (
                f"Opponent won! Board looks like this:\n{self.observe_board()}\n"
                f"You have made {self.llm_num_moves} moves"
            )

        return (
            f"The board now looks like:\n{self.observe_board()}\n"
            f"You have made {self.llm_num_moves} moves"
        )

    def opponent_move(self) -> None:
        row, col = random.choice(list(zip(*np.where(self.board == " "))))
        self.board[row, col] = "O"

    def check_if_a_player_won(self, marker: str) -> bool:
        for row in range(3):
            if (self.board[row, :] == marker).all():
                return True
        for col in range(3):
            if (self.board[:, col] == marker).all():
                return True
        if (np.diagonal(self.board) == marker).all():
            return True
        if np.diag(np.fliplr(self.board) == marker).all():
            return True
        return False

    def check_if_llm_won(self) -> str:
        """Check if you won or not"""
        if self.check_if_a_player_won(marker="X"):
            return "Yes, you have won!"
        else:
            return "No, the game has not finished yet"
