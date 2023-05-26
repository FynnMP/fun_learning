# Import pygame for building the game.
# The random library is used for shuffling graphics and generating random numbers.
# The os library provides functions for interacting with the operating system.
# The json library is used for reading and writing JSON files.
# The Image module from the PIL (Python Imaging Library) is imported for image processing.
import pygame, random, os, json
from PIL import Image

# The Tile class is a subclass of pygame.sprite.Sprite and represents a memory tile in the game.
# It has attributes like name, original_image, back_image, image, rect, and shown.
class Tile(pygame.sprite.Sprite):
    # The __init__ method initializes these attributes based on the given filename, x, and y coordinates.
    def __init__(self, filename, x, y):
        super().__init__()

        # Extract the name from the filename
        self.name = filename.split('_')[0]

        # Load the original image from the given filename
        self.original_image = self.load_image('graphic/memory/content_management/' + filename)

        # Load the back image of the tile (the image displayed when it's not shown)
        self.back_image = pygame.image.load('graphic/memory/0_unisg.png').convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (80, 80)) # Scale the image to the desired size

        self.image = self.back_image  # Set the initial image as the back image
        self.rect = self.image.get_rect(topleft=(x, y))  # Set the rectangle position of the tile
        self.shown = False  # Set the initial shown state of the tile as False (not flipped)

    # The load_image method loads an image from the given path and converts it to the appropriate format using PIL and Pygame.
    def load_image(self, path):
        image = Image.open(path)
        image = image.convert("RGBA") # Convert the image to the correct format (RGBA)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

    # The update method updates the image of the tile based on whether it is shown or not.
    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    # The show method changes the shown attribute of the tile.
    def show(self):
        self.shown = True

    # The hide method changes the shown attribute of the tile.
    def hide(self):
        self.shown = False


# The Game class represents the game itself and contains various methods and attributes related to the game.
class Game():
    # The __init__ method initializes the game state and loads necessary resources.
    # It reads the current score from a JSON file named "wallet.json" and sets it as the initial score.
    # It sets up fonts, graphics, tile dimensions, and other game-related parameters.
    # It creates an empty sprite group for tiles.
    def __init__(self):
        with open("wallet.json", "r") as wallet:
            wallet = json.load(wallet) # Load the content of "wallet.json" into the 'wallet' variable
            self.score = sum(wallet["money"]) # Calculate the sum of the "money" values in the wallet JSON

        self.content_font = pygame.font.Font('graphic/memory/fonts/font.ttf', 12) # Load a custom font

        self.level = 1 # Set the initial level to 1
        self.level_complete = False # Set the initial level completion status to False

        # Graphics that are shown on the tiles.
        self.all_graphics = [f for f in os.listdir('graphic/memory/content_management') if
                             os.path.isfile(os.path.join('graphic/memory/content_management', f)) and f.endswith(
                                 ('.png', '.jpg', '.jpeg'))] # Create a list of filenames of graphics that end with ".png", ".jpg", or ".jpeg" in the "graphic/memory/content_management" directory

        # sort list with all possible memory cards by number
        def custom_sort_key(file_name):
            file_number = int(file_name.split('_')[0]) # Extract the numeric part of the filename
            file_suffix = file_name.split('_')[1] # Extract the suffix (question or answer) of the filename
            # Multiply the number by 2 for "question" files and add 1 for "answer" files
            if file_suffix == 'question.png':
                return file_number * 2
            else:
                return file_number * 2 + 1

        # finally sorting list of all memory cards
        self.all_graphics = sorted(self.all_graphics, key=custom_sort_key)

        self.img_width, self.img_height = (80, 80)  # Set the width and height of the images used for tiles
        self.padding = 20  # Set the padding between tiles
        self.margin_top = 160  # Set the top margin for the tiles
        self.cols = 4  # Set the number of columns for the tile grid
        self.rows = 2  # Set the number of rows for the tile grid
        self.width = 600  # Set the width of the game window

        self.tiles_group = pygame.sprite.Group()  # Create an empty sprite group to store the tiles

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level(self.level)

        # initialize image
        self.background_image = pygame.image.load('graphic/memory/square.jpg').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_HEIGHT, WINDOW_WIDTH))

    # The increase_score method updates the game score.
    def increase_score(self):
        self.score += 5

    # The decrease_score method updates the game score.
    def decrease_score(self):
        self.score -= 5
        if self.score < 0:
            self.score = 0

    # The resize_image method resizes an image using PIL and converts it back to a Pygame surface.
    def resize_image(self, image, size):
        pil_image = Image.fromarray(image) # Convert the image array to a PIL Image object
        resized_image = pil_image.resize(size) # Resize the image using the specified size
        return pygame.surfarray.array3d(resized_image) # Convert the resized image back to a Pygame surface array

    # The update method handles user input, draws the game elements on the screen, and checks for level completion.
    def update(self, event_list):
        self.user_input(event_list) # Handle user input events
        self.draw() # Draw game elements on the screen
        self.check_level_complete(event_list) # Check for level completion

    # The check_level_complete method checks if the level is complete by checking the flipped tiles.
    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos) and not tile.shown:
                            self.flipped.append(tile.name) # Add the name of the flipped tile to the list
                            tile.show() # Show the flipped tile
                            if len(self.flipped) == 2: # Check if two tiles have been flipped
                                if self.flipped[0] != self.flipped[1]: # Check if the flipped tiles are not a match
                                    self.block_game = True # Block further interaction with the tiles
                                    # Decrease score if wrong card chosen (can be applied if wished).
                                    # self.decrease_score()
                                else: # The flipped tiles are a match
                                    self.flipped = [] # Clear the list of flipped tiles
                                    self.increase_score() # Increase score.

                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True # Set level_complete to True if all tiles are shown
                                        else:
                                            self.level_complete = False # Set level_complete to False if any tile is not shown
                                            break
        else:
            self.frame_count += 1 # Increase the frame count
            if self.frame_count == FPS: # If the frame count reaches the desired value (FPS)
                self.frame_count = 0 # Reset the frame count to 0
                self.block_game = False # Unblock interaction with the tiles

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide() # Hide the previously flipped tiles
                self.flipped = [] # Clear the list of flipped tiles

    # The generate_level method generates a new level with random graphics and sets the necessary game state.
    def generate_level(self, level):
        self.graphics = self.select_random_graphics(self.level) # Select random graphics for the level
        self.level_complete = False # Reset the level completion status to False
        self.rows = self.level + 1 # Set the number of rows for the level based on the current level
        self.cols = 4 # Set the number of columns for the level
        self.generate_tileset(self.graphics) # Generate the tileset for the level using the selected graphic

    # The generate_tileset method generates the tileset based on the given graphics.
    def generate_tileset(self, graphics):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows # Set the number of columns and rows to be the maximum of the two

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3) # Calculate the total width of the tileset
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2 # Calculate the left and right margins for centering the tileset
        self.tiles_group.empty() # Clear the existing tiles from the tiles_group

        for i in range(len(graphics)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols)) # Calculate the x-coordinate of the tile based on its position in the grid
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding)) # Calculate the y-coordinate of the tile based on its position in the grid
            tile = Tile(graphics[i], x, y) # Create a new Tile object with the corresponding graphic and coordinates
            self.tiles_group.add(tile) # Add the tile to the tiles_group

    # The select_random_graphics method selects a random set of graphics for the level.
    def select_random_graphics(self, level):
        graphics = [] # Create an empty list to store the selected graphics
        graphics_filter = random.sample(range(0, 24, 2), (self.level + self.level + 2)) # Generate a random sample of indices from the range [0, 24) with a step of 2
        for i in graphics_filter:
            graphics.append(self.all_graphics[i]) # Add the graphic at index i to the graphics list
            graphics.append(self.all_graphics[i + 1]) # Add the next graphic after the one at index i to the graphics list
        random.shuffle(graphics) # Shuffle the order of the graphics in the list
        return graphics # Return the selected and shuffled graphics list

    # The user_input method handles user input events and progresses to the next level.
    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN: # Check if the event is a key press
                if event.key == pygame.K_SPACE and self.level_complete: # Check if the key is the spacebar and the level is complete
                    self.level += 1 # Increase the level by 1
                    if self.level >= 5: # If the level exceeds 4
                        self.level = 1 # Reset the level to 1
                    self.generate_level(self.level) # Generate a new level based on the updated level

    # The draw method draws various game elements on the screen using Pygame's drawing functions.
    def draw(self):
        screen.fill(BLACK) # Fill the screen with a black color

        # fonts
        title_font = pygame.font.Font('graphic/memory/fonts/font.ttf', 20) # Load a custom font with size 20 for title
        content_font = pygame.font.Font('graphic/memory/fonts/font.ttf', 12) # Load a custom font with size 12 for content
        default_font = pygame.font.SysFont(None, 20) # Use the system's default font with size 20
        default_font2 = pygame.font.SysFont(None, 30) # Use the system's default font with size 30

        # background
        screen.blit(self.background_image, (0, 0)) # Draw the background image at position (0, 0)

        score_text = default_font.render("Current balance: $" + str(self.score), True, BLACK) # Render the score text
        score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 30, 20)) # Get the rect for score text
        screen.blit(score_text, score_rect) # Draw the score text on the screen

        # text
        title_text = title_font.render('Memory Game', True, BLACK) # Render the title text
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10)) # Get the rect for title text

        level_text = content_font.render('Level ' + str(self.level), True, BLACK) # Render the level text
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 40)) # Get the rect for level text

        info_text = content_font.render('Find the matching answer to the questions.', True, BLACK) # Render the info text
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80)) # Get the rect for info text

        if not self.level == 4:
            next_text = default_font2.render('Level complete! Press space for next level.', True, WHITE) # Render the next level text
        else:
            next_text = default_font2.render('Congrats! You Won! Press space to play again.', True, WHITE) # Render the game won text
        next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)) # Get the rect for next text

        screen.blit(title_text, title_rect) # Draw the title text on the screen
        screen.blit(level_text, level_rect) # Draw the level text on the screen
        screen.blit(info_text, info_rect) # Draw the info text on the screen

        # draw tileset
        self.tiles_group.draw(screen) # Draw the tiles on the screen
        self.tiles_group.update() # Update the tile positions

        if self.level_complete:
            screen.blit(next_text, next_rect) # Draw the next text on the screen if the level is complete


# Initializing the Pygame.
pygame.init()

# Setting up the window.
WINDOW_WIDTH = 600 # Set the width of the window to 600 pixels
WINDOW_HEIGHT = 600 # Set the height of the window to 600 pixels
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Create the window with the specified dimensions
pygame.display.set_caption('Memory Game') # Set the window caption to 'Memory Game'

WHITE = (255, 255, 255) # Define the color white with RGB values (255, 255, 255)
RED = (255, 0, 0) # Define the color red with RGB values (255, 0, 0)
BLACK = (0, 0, 0) # Define the color black with RGB values (0, 0, 0)

FPS = 60 # Set the frames per second to 60
clock = pygame.time.Clock() # Create a clock object to control the frame rate

# Creating an instance of the Game class.
game = Game()

# Running the game loop.
running = True

# Handling Pygame events and updating the game.
while running:
    # The code retrieves a list of all Pygame events and iterates over them.
    event_list = pygame.event.get() # Get a list of all Pygame events
    for event in event_list: # Iterate over each event in the list
        # If the event type is pygame.QUIT (the user closed the game window), the game loop is stopped.
        if event.type == pygame.QUIT: # Check if the event type is pygame.QUIT
            # Save the current score to the wallet.json file.
            with open("wallet.json", "w") as jsonFile: # Open the wallet.json file in write mode
                money = [] # Create an empty list to store the score
                new_balance = game.score # Get the current score from the game object
                money.append(int(round(float(new_balance)))) # Append the score to the money list
                wallet = {} # Create a dictionary to store the money list
                wallet["money"] = money # Assign the money list to the money key in the dictionary
                json.dump(wallet, jsonFile) # Write the dictionary to the JSON file

            running = False # Set the running flag to False to exit the game loop

    # The game.update() method is called to update the game state based on the events.
    game.update(event_list)

    # The pygame.display.update() function updates the contents of the entire display.
    pygame.display.update()
    # The clock.tick(FPS) method regulates the frame rate of the game.
    clock.tick(FPS)

# The pygame.quit() function uninitializes all Pygame modules.
# This line is executed after the game loop ends, terminating the program.
pygame.quit()
