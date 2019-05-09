"""
Interactive visualization of BFS as a wild fire
Click on the canvas to add orange cells to boundary of the fire (BFS queue)
Click step to advance search, orange cells are on fire (visited by BFS search)
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Global constants
CELL_SIZE = 10
EMPTY = 0 
FULL = 1


class WildFireGUI:
    """
    Container for interactive content
    """    

    def __init__(self, wildfire):
        """ 
        Create frame and timers, register event handlers
        """
        self._fire = wildfire
        self._grid_height = self._fire.get_grid_height()
        self._grid_width = self._fire.get_grid_width()
        self._frame = simplegui.create_frame("Interactive BFS demo", 
                                            self._grid_width * CELL_SIZE, self._grid_height * CELL_SIZE)
        self._frame.set_canvas_background("White")
        self._frame.add_button("Clear all", self.clear, 100)
        self._frame.add_button("Step", self.step, 100)
        self._frame.add_button("Ten steps", self.ten_steps, 100)
        self._frame.set_mouseclick_handler(self.add_cell_index)
        self._frame.set_draw_handler(self.draw)
       
        
    def start(self):
        """
        Start frame
        """
        self._frame.start()
                  
        
    def clear(self):
        """ 
        Event handler for button that clears everything
        """
        self._fire.clear()
    
        
    def step(self):
        """ 
        Event handler for button that add cells to the boundary of the fire
        """
        if self._fire.boundary_size() > 0:
            self._fire.update_boundary()
        else:
            print( "Click in the canvas to cells to the boundary of the fire")

    def ten_steps(self):
        """ 
        Event handler for button that updates the fire boundary by 10 steps
        """
        for dummy_idx in range(10):
            if self._fire.boundary_size() > 0:
                self._fire.update_boundary()
            
    def add_cell_index(self, click_position):
        """ 
        Event handler to add new cell index to the fire boundary
        """
        cell_index = self._fire.get_index(click_position, CELL_SIZE)
        self._fire.set_full(cell_index[0], cell_index[1])
        self._fire.enqueue_boundary(cell_index[0], cell_index[1])
    
    def draw_cell(self, canvas, row, col, color = "Yellow"):
        """
        Draw a cell in the grid
        """
        upper_left = [col * CELL_SIZE, row * CELL_SIZE]
        upper_right = [(col + 1) * CELL_SIZE, row * CELL_SIZE]
        lower_right = [(col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE]
        lower_left = [col * CELL_SIZE, (row + 1) * CELL_SIZE]
        canvas.draw_polygon([upper_left, upper_right, lower_right, lower_left], 1, "Black", color)
    
    def draw_grid(self, canvas, color = "Yellow"):
        """
        Draw entire grid
        """
        for col in range(self._grid_width):
            for row in range(self._grid_height):
                if not self._fire.is_empty(row, col):
                    self.draw_cell(canvas, row, col, color)
             
    def draw(self, canvas):
        """
        Handler for drawing grid
        """        
        self.draw_grid(canvas)
        
        for cell in self._fire.fire_boundary():
            self.draw_cell(canvas, cell[0], cell[1], "Orange")
      
      
# Start interactive simulation    
def run_gui(wildfire):
    """
    Encapsulate frame
    """
    gui = WildFireGUI(wildfire)
    gui.start()
