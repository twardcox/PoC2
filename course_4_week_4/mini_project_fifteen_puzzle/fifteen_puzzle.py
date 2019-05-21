"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui


class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers.

        Finds the position of the tile that belongs at solved_row, solved_col
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    def gen_zero_move_string(self, target_row, target_col,):
        """
        genertes move string for zero from start position to
        target number postition
        """
        move_string = ""

        target_tile_loc = self.current_position(target_row, target_col)
        row_diff = target_tile_loc[0] - target_row
        col_diff = target_tile_loc[1] - target_col
        if row_diff > 0:
            for dummy_row in range(0, row_diff):
                move_string += "d"
        if row_diff < 0:
            for dummy_row in range(0, abs(row_diff)):
                move_string += "u"
        if col_diff > 0:
            for dummy_col in range(0, col_diff):
                move_string += "r"
        if col_diff < 0:
            for dummy_col in range(0, abs(col_diff)):
                move_string += "l"
        return move_string

def get_move_string(self, src_row, src_col, dest_row, dest_col):
        """
        Converts starting tile position, target tile position into move string
        """
        move_string = ""
        x_dist = dest_row - src_row
        y_dist = dest_col - src_col
        if x_dist > 0:
            for dummy_x in range(0, x_dist):
                move_string += "d"
        if x_dist < 0:
            for dummy_x in range(0, abs(x_dist)):
                move_string += "u"
        if y_dist > 0:
            for dummy_y in range(0, y_dist):
                move_string += "r"
        if y_dist < 0:
            for dummy_y in range(0, abs(y_dist)):
                move_string += "l"
        return move_string

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean

        possible variants: row > 1,
        """

        if self.get_number(target_row, target_col):
            return False
        # It's easier to solve this problem in a different space, so
        # let's convert from a row,col grid to a linear space by the
        # following map: i = row * self.get_width() + col
        for dummy_i in range(target_row * self.get_width() + target_col + 1, self.get_width() * self.get_height() - 1):
            col = dummy_i % self.get_width()
            row = int(dummy_i / self.get_width())
            curr_num = self.get_number(row, col)
            if curr_num is not dummy_i:
                return False

        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        target_row, target_col are the location of the tile
        to be solved and the zero tile
        """

        move_str = ""

        # get current position of target
        curr_trgt = self.current_position(target_row, target_col)

        # if currently in correct position. zero at 0,0
        if ([0], curr_trgt[1]) == (target_row, target_col):
            zero_move = self.gen_zero_move_string(target_row, target_col - 1)
            move_str += zero_move
            self.update_puzzle(zero_move)

            return move_str

        # moves zero to target postion
        if target_row == self.get_height()-1 and target_col == self.get_width()-1:
            zero_move = self.gen_zero_move_string(target_row, target_col)
            move_str += zero_move
            self.update_puzzle(zero_move)

        assert self.lower_row_invariant(
            target_row, target_col), "Start zero not in correct position"

        move_str += self.execute_move(curr_trgt[0],
                                      curr_trgt[1], target_row, target_col)

        assert self.lower_row_invariant(
            target_row, target_col - 1), "End zero not in correct postion"
        return move_str

    def execute_move(self, start_row, start_col, target_row, target_col):
        """
        Moves a tile from start position to target position
        Updates puzzle and returns a move string
        """

        move_str = ""
        tile_number = self.get_number(start_row, start_col)

        # new target position
        solved_pos = self.current_position(target_row, target_col)

        # move 0 to target tile
        zero_move = self.gen_zero_move_string(solved_pos[0], solved_pos[1])
        move_str += zero_move
        self.update_puzzle(zero_move)

        # we are done
        if self.get_number(target_row, target_col) == tile_number:
            zero_pos = self.current_position(0, 0)
           
            if (zero_pos[0], zero_pos[0]) == (target_row - 1, target_col):
                move_str += "ld"
                self.update_puzzle("ld")
            return move_str

        # 0 on same row to left
        curr_row, curr_col = self.current_position(
            solved_pos[0], solved_pos[1])
        curr_row, curr_col = self.current_position(
            solved_pos[0], solved_pos[1])

            
        if zero_pos[0] == curr_row:
            move_str += self._shift_right(curr_row,
                                          curr_col, target_row, target_col)
        if self.get_number(target_row, target_col) == tile_number:
            return move_str
        curr_row, curr_col = self.current_position(
            solved_pos[0], solved_pos[1])
        move_str += self._cycle_horizontal(tile_number,
                                           curr_row, curr_col, target_row, target_col)
        while (self.get_number(target_row, target_col) != tile_number):
            zero_pos[0], zero_pos[0] = self.current_position(0, 0)
            curr_row, curr_col = self.current_position(
                solved_pos[0], solved_pos[1])
            relative_pos = self.relative_pos(
                (zero_pos[0], zero_pos[0]), (curr_row, curr_col))
            if relative_pos == "r":
                move_str += "dlu"
                self.update_puzzle("dlu")
            if relative_pos == "u":
                move_str += "lddru"
                self.update_puzzle("lddru")
            if relative_pos == "l":
                move_str += "dru"
                self.update_puzzle("dru")
        zero_pos[0], zero_pos[0] = self.current_position(0, 0)
        if (zero_pos[0], zero_pos[0]) == (target_row - 1, target_col):
            move_str += "ld"
            self.update_puzzle("ld")
        return move_str

    def _cycle_horizontal(self, tile_number, curr_row, curr_col, target_row, target_col):
        """
        Cycles the target tile to left or right 
        Updates puzzle and returns a move string
        """
        move_str = ""
        solved_row, solved_col = self.solved_position(tile_number)
        while (curr_col != target_col):
            zero_row, zero_tile_col = self.current_position(0, 0)
            curr_row, curr_col = self.current_position(solved_row, solved_col)
            relative_pos = self.relative_pos(
                (zero_row, zero_tile_col), (curr_row, curr_col))
            if (curr_col > target_col):
                if relative_pos == "r":
                    move_str += "dllur"
                    self.update_puzzle("dllur")
                if relative_pos == "u":
                    move_str += "ldr"
                    self.update_puzzle("ldr")
                if relative_pos == "d":
                    move_str += "lur"
                    self.update_puzzle("lur")
            if (curr_col < target_col):
                if relative_pos == "u":
                    move_str += "rdl"
                    self.update_puzzle("rdl")
                if relative_pos == "l":
                    move_str += "drrul"
                    self.update_puzzle("drrul")
                if relative_pos == "d":
                    move_str += "rul"
                    self.update_puzzle("rul")
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """

        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""


# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
