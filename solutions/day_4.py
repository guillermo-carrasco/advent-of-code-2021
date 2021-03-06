"""
--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any
sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen
number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or
any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically
generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows
(shown here adjacent to each other to save space):

22 13 17 *11*  0           3 15  0  2 22         14 21 17 24  *4*
 8  2 23  *4* 24           9 18 13 17  *5*       10 16 15  *9* 19
21  *9* 14 16  *7*         19  8  *7* 25 23      18  8 23 26 20
 6 10  3 18  *5*           20 *11* 10 24  *4*    22 *11* 13  6  *5*
 1 12 20 15 19             14 21 16 12  6        2  0 12  3  *7*

Finally, after 24 is drawn the third board wins because it has at least one complete row or column of marked numbers
(in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board;
in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24,
to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first.
What will your final score be if you choose that board?

--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms,
the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards
it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle
column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked
numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
"""
from pydantic import BaseModel
from pathlib import Path


class BingoCell(BaseModel):
    number: int
    marked: bool = False


class Day4(object):
    def __init__(self, input_file_path: Path):
        with open(input_file_path, "r") as f:
            raw_input = f.read().strip().split("\n")

        self.bingo_numbers = [int(n) for n in raw_input[0].split(",")]
        self.boards = []

        current_board = []
        for line in raw_input[2:]:
            if not line:
                self.boards.append(current_board)
                current_board = []
            else:
                row = [BingoCell(number=int(n)) for n in line.split(" ")]
                current_board.append(row)

        # Append the last of the boards
        self.boards.append(current_board)

        self.grid_size = 5
        self.n_boards = len(self.boards)

    def check_row_complete(self, board_index: int, row_index: int):
        return all([cell.marked for cell in self.boards[board_index][row_index]])

    def check_column_complete(self, board_index: int, col_index: int):
        col_aux = []
        for row in self.boards[board_index]:
            col_aux.append(row[col_index].marked)
        return all(col_aux)

    def mark(self, board_index: int, row_index: int, col_index: int):
        self.boards[board_index][row_index][col_index].marked = True

    def check_number_in_board(self, board_index: int, n: int):
        positions = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.boards[board_index][i][j].number == n:
                    positions.append((i, j))
        return positions

    def score(self, board_index, last_num):
        score = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if not self.boards[board_index][i][j].marked:
                    score += self.boards[board_index][i][j].number

        return last_num * score

    def _play_bingo(self, first_win=True):
        already_won = set()
        score = -1
        for n in self.bingo_numbers:
            for board_index in range(self.n_boards):
                if board_index not in already_won:
                    positions = self.check_number_in_board(board_index, n)
                    # If there are matches, mark them and immediately check for completeness after marking them
                    for row, col in positions:
                        self.mark(board_index, row, col)
                        if self.check_row_complete(board_index, row) or self.check_column_complete(board_index, col):
                            if first_win:
                                return self.score(board_index, n)
                            else:
                                score = self.score(board_index, n)
                                already_won.add(board_index)
        return score

    def part_1(self):
        return self._play_bingo(first_win=True)

    def part_2(self):
        return self._play_bingo(first_win=False)
