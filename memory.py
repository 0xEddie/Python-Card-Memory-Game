"""Memory Version 3"""
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
        self.pause_time = 0.0001 # smaller is faster game
        self.close_clicked = False
        self.continue_game = True
        self.image_list = []
        self.create_image_list()
        self.board = []
        self.create_board()
        self.score = 0
        self.flipped_counter = 0
        self.tile1, self.tile2 = None, None
    
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
        # Handle each user event by changing the game state appropriately
        # - self is the Game whose events will be handled.
        event = pygame.event.poll()
        # close the game if someone has clicked on the close button
        if event.type == QUIT:
            self.close_clicked = True
        if event.type == MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event.pos)
            
        
    def handle_mouse_up(self, click_position):
        # flips an unexposed tile when mouse left button is released from 
        # down clicked position
        # - self: the Game the mouse is being clicked on
        # - click_positon: the coords of the mouse from a MOUSEBUTTONUP event
        for row in self.board:
            for tile in row:
                if tile.select(click_position):
                    tile.expose()
                    if self.tile1 is None and self.tile2 is None:
                        self.tile1 = tile
                    elif self.tile1 is not None and self.tile2 is None:
                        self.tile2 = tile
                
            
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw        
        self.window.clear()
        
        # draw each of our tiles
        for row in self.board:
            for tile in row:
                tile.draw()
        self.draw_score()
        self.window.update()
        
    def draw_score(self):
        # draws the score in the right panel in the window
        # - self: the Game to draw on
        font_size = 70
        self.window.set_font_size(font_size)
        self.window.set_font_color('white')
        string_x = self.window.get_width() - self.window.get_string_width(str(self.score))
        string_y = 0
        display_string = str(self.score)
        self.window.draw_string(display_string,string_x,string_y)
    
    def update(self):
        # Update the game objects.
        # - self: the Game to update
        self.score = pygame.time.get_ticks()//1000
        self.compare()
        
    def compare(self):
        # compares contents of selected tiles
        # - self: the Game containing the selected tiles
        if self.tile1 is not None and self.tile2 is not None:
            if self.tile1 == self.tile2:
                self.flipped_counter += 2
            else:
                time.sleep(1)
                self.tile1.flip()
                self.tile2.flip()
            self.tile1, self.tile2 = None, None
         
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self: the Game to check
        if self.flipped_counter > 15:
            self.continue_game = False

class Tile:
    # represents a single tile on a Tic Tac Toe board
    
    # Class Attributes
    border_width = 5
    window = None
    cover_image = pygame.image.load('image0.bmp')
    
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
        self.under_image = image 
        # the window to draw our tile to
        self.surface = Tile.window.get_surface()
        self.exposed = False
        
    def __eq__(self,other):
        # comparison of image contents of tile instances
        # - self: first tile selected
        # - other: second tile selected
        match = False
        if self.under_image == other.under_image:
            match = True
        return match
        
    def draw(self):
        # draws our tile contents and borders to the screen
        #   - self: the tile to draw
        
        # draw borders
        rect_color = pygame.Color('black')
        pygame.draw.rect(self.surface, rect_color, self.rect, Tile.border_width)
        
        # draw image to tile
        if self.exposed:
            self.surface.blit(self.under_image, self.rect)
        else:
            self.surface.blit(Tile.cover_image, self.rect)
            
    def expose(self):
        # set tile exposure to True
        # - self: the Tile to expose
        self.exposed = True
        
    def flip(self):
        # set tile exposure to False
        # - self: the Tile to unexpose
        self.exposed = False  
    
    def select(self,position):
        # flips tile if mouse is on tile during MOUSEBUTTONUP event, and if the
        # tile is not already exposed
        # - self: the Tile to flip
        # - position: the position of the mouse during MOUSEBUTTONUP event
        return (self.rect.collidepoint(position) and not self.exposed)
            
main()