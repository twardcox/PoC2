"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
##        self._grid_height = grid_height
##        self._grid_width = grid_width
#        self._obstacle_list = obstacle_list
        
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        #pass
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append( (row, col) )
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie 
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append( (row, col) )
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human 
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        
        #1) Create a new grid visited of the same size as the original 
        #grid and initialize its cells to be empty.
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        
        #2)
        distance_field = [[self._grid_width * self._grid_height \
                                for dummy_col in range(self._grid_width)]  \
                                    for dummy_row in range(self._grid_height)]
        
        #3)
        boundary = poc_queue.Queue()
        #if entity_type == 'ZOMBIE':
        entity_list = self._zombie_list if entity_type == ZOMBIE else self._human_list
        for element in entity_list:
            boundary.enqueue(element)
            visited.set_full(element[0],element[1])
            distance_field[element[0]][element[1]] = 0
#        else:
#            for element in self._human_list:
#                Que.enqueue(element)
#                visited.set_full(element[0],element[1])
#                distance_field[element[0]][element[1]] = 0
#        #4)
        
#        while boundary is not empty:
        while len(boundary) > 0:
#            current_cell  ←  dequeue boundary
            current_cell = boundary.dequeue()
#            for all neighbor_cell of current_cell:
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:
#                if neighbor_cell is not in visited:
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    #if passable
                    if self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    #if neighbor_cell not in self._obstacle_list:
    #                    add neighbor_cell to visited
    #                    enqueue neighbor_cell onto boundary
                        visited.set_full(neighbor_cell[0], neighbor_cell[1])
                        boundary.enqueue(neighbor_cell)
                        distance_field[neighbor_cell[0]][neighbor_cell[1]] = \
                            distance_field[current_cell[0]][current_cell[1]] + 1
        
        return distance_field
    
    ### MANGEL ER : [line 155] Too many branches (25/12) - I FUNKTIONEN!
    # LØSNING ER DEFINER zombie_distance_field[row][col] I ALLE DE FORSK
    # SKAL OGSÅ GØRES I MOVE_ZOMBIES
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for human in self._human_list:
            row, col = human[0], human[1]
            optimum = (row, col)
            dist = zombie_distance_field[row][col] 
            
            for neigbor in self.eight_neighbors(row, col):
                row_n, col_n = neigbor[0], neigbor[1] 
                if self.is_empty(row_n,col_n) and \
                 zombie_distance_field[row_n][col_n] > dist:
                        optimum = (row_n, col_n)
                        dist = zombie_distance_field[row_n][col_n]             
#            if row > 0:
#                if zombie_distance_field[row - 1][col] > dist:
#                    if self.is_empty(row - 1,col):
#                        optimum = (row-1, col)
#                        dist = zombie_distance_field[row-1][col]     
#            if row < self._grid_height - 1:
#                if zombie_distance_field[row + 1][col] > dist:
#                    if self.is_empty(row+1,col):
#                        optimum = (row+1, col)
#                        dist = zombie_distance_field[row+1][col]     
#            if col > 0:
#                if zombie_distance_field[row][col-1] > dist:
#                    if self.is_empty(row,col-1):
#                        optimum = (row, col-1)
#                        dist = zombie_distance_field[row][col-1]     
#                        #ans.append((row, col - 1))
#            if col < self._grid_width - 1:
#                if zombie_distance_field[row][col+1] > dist:
#                    if self.is_empty(row,col+1):
#                        optimum = (row, col+1)
#                        dist = zombie_distance_field[row][col+1]     
#                #ans.append((row, col + 1))
#            if (row > 0) and (col > 0):
#                if zombie_distance_field[row-1][col-1] > dist:
#                    if self.is_empty(row-1,col-1):
#                        optimum = (row-1, col-1)
#                        dist = zombie_distance_field[row-1][col-1]     
#                #ans.append((row - 1, col - 1))
#            if (row > 0) and (col < self._grid_width - 1):
#                if zombie_distance_field[row-1][col+1] > dist:
#                    if self.is_empty(row-1,col+1):
#                        optimum = (row-1, col+1)
#                        dist = zombie_distance_field[row-1][col+1]     
#                #ans.append((row - 1, col + 1))
#            if (row < self._grid_height - 1) and (col > 0):
#                if zombie_distance_field[row+1][col-1] > dist:
#                    if self.is_empty(row+1,col-1):
#                        optimum = (row+1, col-1)
#                        dist = zombie_distance_field[row+1][col-1]     
#                #ans.append((row + 1, col - 1))
#            if (row < self._grid_height - 1) and (col < self._grid_width - 1):
#                if zombie_distance_field[row+1][col+1] > dist:
#                    if self.is_empty(row+1,col+1):
#                        optimum = (row+1, col+1)
#                        dist = zombie_distance_field[row+1][col+1]     
#                #ans.append((row + 1, col + 1))
#                
            new_human_list.append(optimum)
        
        self._human_list = new_human_list
        return 
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        
        for zombie in self._zombie_list:
            row, col = zombie[0], zombie[1]
            optimum = (row, col)
            dist = human_distance_field[row][col] 
            
            for neigbor in self.four_neighbors(row, col):
                row_n, col_n = neigbor[0], neigbor[1] 
                if self.is_empty(row_n,col_n) and \
                 human_distance_field[row_n][col_n] < dist:
                        optimum = (row_n, col_n)
                        dist = human_distance_field[row_n][col_n]     
                                
            
#            
#            if row > 0:
#                if human_distance_field[row - 1][col] < dist:
#                    if self.is_empty(row-1,col):
#                        optimum = (row-1, col)
#                        dist = human_distance_field[row-1][col]     
#            if row < self._grid_height - 1:
#                if human_distance_field[row + 1][col] < dist:
#                    if self.is_empty(row+1,col):
#                        optimum = (row+1, col)
#                        dist = human_distance_field[row+1][col]     
#            if col > 0:
#                if human_distance_field[row][col-1] < dist:
#                    if self.is_empty(row,col-1):
#                        optimum = (row, col-1)
#                        dist = human_distance_field[row][col-1]     
#                    #ans.append((row, col - 1))
#            if col < self._grid_width - 1:
#                if human_distance_field[row][col+1] < dist:
#                    if self.is_empty(row,col+1):
#                        optimum = (row, col+1)
#                        dist = human_distance_field[row][col+1]     

                        
            new_zombie_list.append(optimum)
        
        self._zombie_list = new_zombie_list
        return 
    
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#obj = Apocalypse(3, 3, [(0, 0), (0, 1), (0, 2), (1, 0)], [(2, 1)], [(1, 1)])
#poc_zombie_gui.run_gui(obj)

poc_zombie_gui.run_gui(Apocalypse(30, 40))
