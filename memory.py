"""Memory Version 1"""
import time, pygame, random
from uagame import Window
from pygame.locals import *

# User-defined functions
def main():
    # Creates the game window and game, and runs game

    window = Window('Memory', 500, 400)
    window.set_auto_update(False)
    game = Game(window)
    game.play()
    window.close()

# User-defined classes

class Game:
    # Defines a game of Tic Tac Toe

    def __init__(self, window):
        # Initialize a Game.
        # - self is the Game to initialize
        # - window is the uagame window object
        
        # create all of the game attributes
        self.window = window
        Tile.set_window(window)        
        self.pause_time = 0.04 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True 
        self.image_list = []
        self.create_image_list()
        self.board = [ ]
        self.create_board()
    
    def create_image_list(self):
        # creates and shuffles the list of images
        # - self: the Game to create images for
        for i in range(1,9):
            filename = 'image' + str(i) + '.bmp'
            self.image_list.append(pygame.image.load(filename))
        self.image_list += self.image_list
        random.shuffle(self.image_list)
    
    def create_board(self):
        # creates grid of tiles with images on them
        # - self: the Game to create tiles for        
        width = (self.window.get_width()-100)//4
        height = self.window.get_height()//4
        for row_index in range(4):
            row =[]
            for col_index in range(4):
                x = width * col_index
                y = height * row_index
                image = self.image_list[4 * row_index + col_index]
                tile = Tile(x,y,width,height,image)
                row.append(tile)
            self.board.append(row)    
    
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_event()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time) # set game velocity by pausing
                       
    def handle_event(self):
        # Handle each user event by changing the game state
        # appropriately.image = sset_windowelf.image_list[4*row_index + col_index]
        # - self is the Game whose events will be handled.

        event = pygame.event.poll()
        # close the game if someone has clicked on the close button
        if event.type == QUIT:
            self.close_clicked = True

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw        
        self.window.clear()
        
        # draw each of our tiles
        for row in self.board:
            for tile in row:
                tile.draw()

        self.window.update()
        
    def update(self):
        # Update the game objects.
        # - self is the Game to update
        pass
             
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        pass

class Tile:
    # represents a single on a Tic Tac Toe board
    
    # Class Attributes
    border_width = 5
    window = None
    
    # Class methods
    @classmethod
    def set_window(cls,game_window):
        # referenced class window should be the uagame window
        cls.window = game_window
    
    # Instance methods
    def __init__(self, x, y, width, height, image):
        # attributes related to drawing our rectangle
        self.rect = pygame.Rect(x, y, width, height)
        
        # attributes related to drawing our tile content
        self.content = image
        
        # the window to draw our tile to
        self.surface = Tile.window.get_surface()
        
    def draw(self):
        # draws our tile contents and borders to the screen
        #   - self: the tile to draw
        
        # draw borders
        rect_color = pygame.Color('black')
        pygame.draw.rect(self.surface, rect_color, self.rect, Tile.border_width)
        
        # draw image to tile
        self.surface.blit(self.content, self.rect)
    
main()