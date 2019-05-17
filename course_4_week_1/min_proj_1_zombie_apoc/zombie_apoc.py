"""
Student portion of Zombie Apocalypse mini-project
"""

import random
from poc_imports import poc_grid
from poc_imports import poc_queue

from poc_imports import poc_zombie_gui

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
        self.__init__(self._grid_height, self._grid_width)
        
        return

        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
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

        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width \
                           for dummy_col in range(self._grid_width)]\
                          for dummy_row in range(self._grid_height)]

        boundary = poc_queue.Queue()


        cast = self._zombie_list if entity_type == ZOMBIE else self._human_list

        for member in cast:
            boundary.enqueue(member)
            visited.set_full(member[0],member[1])
            distance_field[member[0]][member[1]] = 0

        # if entity_type == ZOMBIE:
        #     for zombie in self._zombie_list:
        #         boundary.enqueue(zombie)

        # elif entity_type == HUMAN:
        #     for human in self._human_list:
        #         boundary.enqueue(human)

        # for side in boundary.__iter__():
        #     visited.set_full(side[0], side[1])
        #     distance_field[side[0]][side[1]] = 0

        while bool(boundary):
            current_cell = boundary.dequeue()

            if entity_type == ZOMBIE:
                neighbors = visited.four_neighbors(current_cell[0], current_cell[1])

            else:
                neighbors = visited.eight_neighbors(current_cell[0], current_cell[1])

            for neighbor in neighbors:

                if self.is_empty(neighbor[0],neighbor[1]) and visited.is_empty(neighbor[0], neighbor[1]):
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)

        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in range(len(self._human_list)):

            highest_num = float('-inf')
            possible_moves = self.eight_neighbors(self._human_list[human][0], self._human_list[human][1])

            possible_moves.append(self._human_list[human])

            for human_num in possible_moves:

                if (zombie_distance_field[human_num[0]][human_num[1]] > highest_num) and self.is_empty(human_num[0],human_num[1]):
                    highest_num = zombie_distance_field[human_num[0]][human_num[1]]
                    self._human_list[human] = human_num
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in range(len(self._zombie_list)):
            lowest_num = float('inf')
            possible_moves = self.four_neighbors(self._zombie_list[zombie][0], self._zombie_list[zombie][1])

            possible_moves.append(self._zombie_list[zombie])

            for zombie_num in possible_moves:
                
                if (human_distance_field[zombie_num[0]][zombie_num[1]] < lowest_num) and self.is_empty(zombie_num[0],zombie_num[1]):
                    lowest_num = human_distance_field[zombie_num[0]][zombie_num[1]]
                    self._zombie_list[zombie] = zombie_num

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
