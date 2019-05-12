"""
Word Wrangler GUI
"""

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Global constants
FONT_SIZE = 20
OFFSET = 4
ROW_HEIGHT = FONT_SIZE + OFFSET
COLUMN_WIDTH = 80
GRID_SIZE = [25, 4]
CANVAS_WIDTH = COLUMN_WIDTH * GRID_SIZE[1]
CANVAS_HEIGHT = ROW_HEIGHT * GRID_SIZE[0]


def draw_word(canvas, word, pos):
    """
    Helper function to draw word on canvas at given position
    """
    box = [pos, 
           [pos[0], pos[1] - ROW_HEIGHT], 
           [pos[0] + COLUMN_WIDTH, pos[1] - ROW_HEIGHT], 
           [pos[0] + COLUMN_WIDTH, pos[1]], 
           pos]
    canvas.draw_text(word, [pos[0] + 2, pos[1] - 4], FONT_SIZE, "White")
    canvas.draw_polyline(box, 1, "White")

class WordWranglerGUI:
    """
    Container for interactive content
    """    

    def __init__(self, game):
        """ 
        Create frame and timers, register event handlers
        """
        self.game = game
        self.frame = simplegui.create_frame("Word Wrangler", 
                                            CANVAS_WIDTH, CANVAS_HEIGHT, 250)
        self.frame.set_canvas_background("Blue")        
               
        self.enter_input = self.frame.add_input("Enter word for new game", 
                                                self.enter_start_word, 250)
        labelmsg = "Stars correspond to hidden words formed using letters "
        labelmsg += "from the entered word. Hidden words are listed in alphabetical order"
        self.frame.add_label(labelmsg, 250)
        self.frame.add_label("", 250)
        self.guess_label = self.frame.add_input("Enter a word", 
                                                self.enter_guess, 250)       
        self.frame.add_label("For a hint, click on a starred word", 250)
        self.frame.set_mouseclick_handler(self.peek)
        self.frame.set_draw_handler(self.draw)

        self.enter_input.set_text("python")
        self.game.start_game("python")
        
    def start(self):
        """
        Start frame
        """
        self.frame.start()
        
    def enter_start_word(self, entered_word):
        """ 
        Event handler for input field to enter letters for new game
        """
        self.game.start_game(entered_word)

    def enter_guess(self, guess):
        """ 
        Event handler for input field to enter guess
        """
        self.game.enter_guess(guess)
        self.guess_label.set_text("")

    def peek(self, pos):
        """ 
        Event handler for mouse click, exposes clicked word
        """
        [index_i, index_j] = [pos[1] // ROW_HEIGHT, pos[0] // COLUMN_WIDTH]
        peek_idx = index_i + index_j * GRID_SIZE[0]
        if peek_idx < len(self.game.get_strings()):
            self.game.peek(peek_idx)
                         
    def draw(self, canvas):
        """
        Handler for drawing subset words list
        """
        string_list = self.game.get_strings()
        
        for col in range(GRID_SIZE[1]):
            for row in range(GRID_SIZE[0]):
                pos = [col * COLUMN_WIDTH, (row + 1) * ROW_HEIGHT]
                idx = row + col * GRID_SIZE[0]
                if idx < len(string_list):
                    draw_word(canvas, string_list[idx], pos)
                      
        # if self.winner_flag:
        #     canvas.draw_text("You win!", 
        #                      [4 * ROW_HEIGHT, COLUMN_WIDTH], 
        #                      2 * FONT_SIZE, "Yellow")
            
# Start interactive simulation    
def run_gui(game):
    """
    Encapsulate frame
    """
    gui = WordWranglerGUI(game)
    gui.start()
    
