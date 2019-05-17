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
        Returns a tuple of two integers        
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

    ##################################################################
    # Phase one methods
    def get_lower_row_invariant_indices(self, target_row, target_col):
        '''
        Returns relevant grid indices to check lower_row_invariant assertion
        '''
        #assert (target_row > 1 and target_row <= self.get_height() - 1
        #        and target_col >= 0 and target_col <= self.get_width()-1), 'Unacceptable taget for get_lower_row_invariant_indices'
        
        return_grid = []
        for _row in range(self.get_height()):
            for _col in range(self.get_width()):
                if (target_col < _col and _row == target_row) or (_row > target_row):
                    return_grid.append((_row, _col))
        
        return return_grid

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        statement_a = target_row == self.get_height() - 1
        statement_b = target_col == self.get_width() - 1
        statement_c = self.get_number(target_row, target_col) == 0
        if (statement_a and statement_b and statement_c):
            return True
        
        if self.get_number(target_row, target_col) != 0:
            return False
        
        invariant_tiles = self.get_lower_row_invariant_indices(target_row, target_col)
        first_index = invariant_tiles[0]
        first_number = self.get_number(first_index[0], first_index[1])
        
        if (first_index[0], first_index[1]) != self.current_position(first_index[0], first_index[1]):
            return False
        
        for tile in invariant_tiles[1:]:
            if self.get_number(tile[0], tile[1]) != first_number + 1:
                return False
            first_number += 1

        return True
    
    def li_get_right(self, target_row, target_col):
        '''
        Moves zero tile to the right of target tile
        '''
        zero_row, zero_col = self.current_position(0,0)
        assert zero_col > target_col, 'Non-senical use of li_get_right()'
        ups = zero_row - target_row
        lefts = zero_col - target_col - 1
        movement_string = ups * 'u' + lefts * 'l'
        self.update_puzzle(movement_string)
        return(movement_string)
        
    def li_get_left(self, target_row, target_col):
        '''
        Moves zero tile to the left of target tile
        '''
        zero_row, zero_col = self.current_position(0,0)
        assert (zero_col < target_col and zero_row > target_row), 'Non-sensical use of li_get_left()'
        ups = zero_row - target_row
        rights = target_col - zero_col - 1
        movement_string = ups * 'u' + rights * 'r'
        self.update_puzzle(movement_string)
        return(movement_string)

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ''
        
        assert self.lower_row_invariant(target_row, target_col), "Lower invariant doesn't holed"
        hit_row, hit_col = self.current_position(target_row, target_col)
        if hit_col < target_col:
            move_string += self.li_get_right(hit_row, hit_col)
            if hit_row == 0:
                self.update_puzzle('dlurd')
                move_string += 'dlurd'
            
            self.update_puzzle('l')
            move_string += 'l'
            while self.current_position(target_row, target_col)[1] != target_col:
                self.update_puzzle('urrdl')
                move_string += 'urrdl'
            while not self.lower_row_invariant(target_row, target_col-1):
                self.update_puzzle('druld')
                move_string += 'druld'
        
        elif hit_col == target_col:
            ups = target_row - hit_row - 1
            self.update_puzzle(ups * 'u' + 'uld')
            move_string += ups * 'u' + 'uld'
            while not self.lower_row_invariant(target_row, target_col-1):
                self.update_puzzle('druld')
                move_string += 'druld'
                       
        else:
            move_string += self.li_get_left(hit_row, hit_col)
            if hit_row == 0:
                self.update_puzzle('druld')
                move_string += 'druld'
            
            self.update_puzzle('r')
            move_string += 'r'
            while self.current_position(target_row, target_col)[1] != target_col:
                self.update_puzzle('ulldr')
                move_string += 'ulldr'
                
            self.update_puzzle('ullddruld')
            move_string += 'ullddruld'
            
            while not self.lower_row_invariant(target_row, target_col-1):
                self.update_puzzle('druld')
                move_string += 'ullddruld'
                
        assert self.lower_row_invariant(target_row, target_col-1), "Lower_row_invariant doesn't hold after moves"
        return move_string
        
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = ''
        
        assert self.lower_row_invariant(target_row, 0), "Lower invariant doesn't holed"
        hit_row, hit_col = self.current_position(target_row, 0)
        
        if hit_col == 0 and hit_row == target_row - 1:
            _temp_string = 'u' + 'r' * int(self.get_width()-1)
            self.update_puzzle(_temp_string)
            move_string += _temp_string
            return move_string
        
        elif hit_col == 0:
            ups = target_row - hit_row - 1
            self.update_puzzle(ups * 'u' + 'urd')
            move_string += ups * 'u' + 'urd'
            while self.current_position(target_row, 0)[0] != target_row - 1:
                self.update_puzzle('dlurd')
                move_string += 'dlurd'
                
            self.update_puzzle('l')
            move_string += 'l'
                       
        elif hit_col > 1:
            move_string += self.li_get_left(hit_row, hit_col)
            if hit_row == 0:
                self.update_puzzle('druld')
                move_string += 'druld'
            
            self.update_puzzle('r')
            move_string += 'r'
            
            while self.current_position(target_row, 0)[1] != 1:
                self.update_puzzle('ulldr')
                move_string += 'ulldr'
            
            while self.current_position(target_row, 0)[0] != target_row - 1:
                self.update_puzzle('dlurd')
                move_string += 'dlurd'
                
            self.update_puzzle('ulld')
            move_string += 'ulld'
            
        else:
            move_string += self.li_get_left(hit_row, hit_col)
            
            while self.current_position(target_row, 0)[0] != target_row - 1:
                self.update_puzzle('druld')
                move_string += 'druld'
        
        _temp_text = 'ruldrdlurdluurddlu' + int(self.get_width() - 1) * 'r'
        self.update_puzzle(_temp_text) 
        move_string += _temp_text
              
        assert self.lower_row_invariant(target_row-1, self.get_width()-1), "Lower_row_invariant doesn't hold after moves"
        return move_string

    #############################################################
    # Phase two methods

    def get_row_invariant_indices(self, target_row, target_col):
        '''
        Generate indices to check in row0_invariant and row1_invariant
        ''' 
        assert target_row < 2 and target_col > 1, 'Invalid parameters for get_row_invariant_indices()'
        
        col_index = target_col
        row_index = target_row
        right_indices = []
        down_indices = []
        
        while col_index < self.get_width():
            right_indices.append((row_index, col_index))
            col_index += 1
        
        col_index = target_col
        row_index += 1
        
        while row_index < self.get_height():
            down_indices.append((row_index, col_index))
            row_index += 1
            
        return right_indices, down_indices
        
    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        indices = self.get_lower_row_invariant_indices(0, target_col)
        row0_indices = indices[:(self.get_width()-target_col-1)]
        other_indices = indices[(self.get_width()-1):]
        base_pos = (0, target_col)
        
        if self.get_number(base_pos[0], base_pos[1]) != 0:
            return False
        
        if target_col != self.get_width() - 1:
            if self.current_position(row0_indices[0][0], row0_indices[0][1]) != (row0_indices[0][0], row0_indices[0][1]):
                return False
        
            row0_init_val = self.get_number(row0_indices[0][0], row0_indices[0][1])

            for tile in row0_indices:
                if self.get_number(tile[0], tile[1]) != row0_init_val:
                    return False
                row0_init_val += 1
        
        
        if self.current_position(other_indices[0][0], other_indices[0][1]) != (other_indices[0][0], other_indices[0][1]):
            return False
        
        other_init_val = self.get_number(other_indices[0][0], other_indices[0][1])
        
        for tile in other_indices:
            if self.get_number(tile[0], tile[1]) != other_init_val:
                return False
            other_init_val += 1
            
        return True
    
    def row1_invariant(self, target_col):
        '''
        Check if row1 invariant holds True
        '''
        return(self.lower_row_invariant(1, target_col))

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        #assert self.row0_invariant(target_col)
        
        solution_string = ''
        hit_row, hit_col = self.current_position(0,target_col)
        
        self.update_puzzle('ld')
        solution_string += 'ld'
        
        if self.current_position(0, target_col) == (0, target_col):
            return solution_string
        
        ### been fukcing around here
        if hit_row == 1 and hit_col == target_col - 1:
            self.update_puzzle('uld')
            solution_string += 'uld'
            self.update_puzzle('urdlurrdluldrruld')
            solution_string += 'urdlurrdluldrruld'
            return solution_string
            
        if hit_row == 0:
            lefts = ((target_col-1)-hit_col)*'l' + 'urdl'
            self.update_puzzle(lefts)
            solution_string += lefts
        
        else:
            lefts = (target_col-hit_col-2)*'l'
            self.update_puzzle(lefts+'l')
            solution_string += lefts+'l'
        
        while self.current_position(0, target_col) != (1, target_col-1):
            self.update_puzzle('urrdl')
            solution_string += 'urrdl'
        
        self.update_puzzle('urdlurrdluldrruld')
        solution_string += 'urdlurrdluldrruld'
        
        return solution_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), 'Row1 invariant is not satisfied in solve_row1_tile'
        solution_string = ''
        hit_row, hit_col = self.current_position(1, target_col)
        
        #get under target
        if hit_row == 0 and hit_col == target_col:
            self.update_puzzle('u')
            solution_string += 'u'
            #assert self.row1_invariant(target_col-1), 'Row1 invariant does not hold after update in solve_row1_tile'
            return solution_string
        
        elif hit_row == 0:
            lefts = (target_col-hit_col)*'l'+'urd'
            self.update_puzzle(lefts)
            solution_string += lefts
            
        else:
            lefts = (target_col-hit_col-1)*'l'
            self.update_puzzle(lefts)
            solution_string += lefts
        
        self.update_puzzle('l')
        solution_string += 'l'
        
        while not self.row1_invariant(target_col-1):
            self.update_puzzle('urrdl')
            solution_string += 'urrdl'
            
        self.update_puzzle('ur')
        solution_string += 'ur'
        
        assert self.row0_invariant(target_col), 'Row0 invariant does not hold after update in solve_row1_tile'   
        
        return solution_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        solution_string = ''
        self.update_puzzle('lu')
        solution_string += 'lu'
        
        while not (self.current_position(0,0) == (0,0) and
                   self.current_position(0,1) == (0,1) and
                   self.current_position(1,0) == (1,0) and
                   self.current_position(1,1) == (1,1)):
            self.update_puzzle('rdlu')
            solution_string += 'rdlu'
        
        return solution_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        solution_string = ''
        #get 0 to bottom left corner
        zero_row, zero_col = self.current_position(0,0)
        rights = self.get_width()-1-zero_col
        downs = self.get_height()-1-zero_row
        self.update_puzzle(rights*'r')
        solution_string += rights*'r'
        self.update_puzzle(downs*'d')
        solution_string += downs*'d'
        
        #self.solve_interior_tile(self.current_position(0,0)[0],self.current_position(0,0)[1])
        for x_ind in range(self.get_height()-1,1,-1):
            for y_ind in range(self.get_width()-1,-1,-1):
                assert self.lower_row_invariant(x_ind,y_ind)
                if y_ind != 0:
                    solution_string += self.solve_interior_tile(x_ind,y_ind)
                    assert self.lower_row_invariant(x_ind,y_ind-1)
                else:
                    solution_string += self.solve_col0_tile(x_ind)
                    assert self.lower_row_invariant(x_ind-1,y_ind+self.get_width()-1)
        
        for y_ind in range(self.get_width()-1,1,-1):            
            assert self.row1_invariant(y_ind)
            solution_string += self.solve_row1_tile(y_ind)
            assert self.row0_invariant(y_ind)
            solution_string += self.solve_row0_tile(y_ind)
        
        solution_string += self.solve_2x2()
        
        
        return solution_string

# Start interactive simulation
#obj = Puzzle(3,3, [[0,1,2], [3,4,5], [0,0,8]])
#obj2 = Puzzle(5,5, [[0,24,23,22,21],[20,19,18,17,16],[15,14,13,12,11],[10,9,8,7,6],[5,4,3,2,1]])
#obj3 = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#poc_fifteen_gui.FifteenGUI(obj)
#obj.solve_puzzle() 
#obj2.solve_row0_tile(4)
#obj2.solve_puzzle()
#obj2.solve_2x2()
#print obj2.row1_invariant(4)
#obj2.solve_row1_tile(4)
#print obj2.solve_row0_tile(4)
#print obj2.solve_col0_tile(4)
#dlurdlurrdldruld
#print obj2.get_row_invariant_indices(0,2)
#print obj2.row0_invariant(3)
#obj = Puzzle(4, 5, [[8, 2, 10, 9, 1], [7, 6, 5, 4, 3], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(obj)
#obj.solve_col0_tile(2) 

#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(obj2)
#print obj2.solve_row0_tile(4)

#print obj2.solve_interior_tile(4,4)
#dlurdlurrdlurrdlurrdldrulddrulddruld
#obj2.lower_row_invariant(3,4)
#obj2.li_get_right(0,0)
#obj2.li_get_left(0,2)
#obj2.get_under()
#print(obj2.lower_row_invariant(1,3))
#print obj2.get_height()
#print(obj.get_lower_row_invariant_indices(2,0))
#print obj2
#print(obj2.lower_row_invariant(3,3))
#print obj
#print(obj.lower_row_invariant(2,1))
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print(obj.lower_row_invariant(2, 2))