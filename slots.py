# Special thanks and credits to notaSWE (https://github.com/notaSWE/pygameslots) for providing the general code framework for this casino game


# Importing modules to work with Windows, game development, systemspecific parameters and functions, random number generation, and JSON
import ctypes, pygame, sys, random, json
# Maintain resolution regardless of Windows scaling settings
# ctypes.windll.user32.SetProcessDPIAware()

# Display settings
#Specifying the default image size
DEFAULT_IMAGE_SIZE = (150, 150)
#Specifying frames per second
FPS = 120
#Specifying height and width of the display window
HEIGHT = 500
WIDTH = 800
#Specifying the starting coordinates for the slot machine grid
START_X, START_Y = 0, -150
#Specifying the offsets for positioning the symbols
X_OFFSET, Y_OFFSET = 10, 0

# The four line code below specify the file paths for different images used in the slot machine
# The background image
BG_IMAGE_PATH = 'graphic/slot/bg.png'
#The image for gridlines
GRID_IMAGE_PATH = 'graphic/slot/gridline.png'
#Indices of the playable area
GAME_INDICES = [1, 2, 3] # 0 and 4 are outside of play area
#Directory path for the symbol images
SYM_PATH = 'graphic/slot/symbols'

# Displaying the text color in the game
TEXT_COLOR = 'White'

# The code below defines a directionary called "symbols"
# Symbol names are mapped to their corresponding file paths
symbols = {
    'coin': f"{SYM_PATH}/0_coin.png", 
    'eth': f"{SYM_PATH}/0_eth.png",
    'sg': f"{SYM_PATH}/0_sg.png",
    'unisg': f"{SYM_PATH}/0_unisg.png",
    'swiss': f"{SYM_PATH}/0_swiss.png"
}



# Definying a class called "Player"
class Player():
#__init__ method initializes the instance variables of the object "Player". 
# This constructor reads the conetnts of the "wallet.json" file   
    def __init__(self):
        with open("wallet.json", "r") as wallet:
            wallet = json.load(wallet)
#The "money" list calculate the initial balance for the player
            money = wallet["money"]
        self.balance = sum(money)
#The other variables below are set to their initial values
        self.bet_size = 5.00
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00
#The method "get_data" returns a dictionary containing the player's data
    def get_data(self):
        player_data = {}
# In the code below the player's data (palyer balance, player bet size, player last payout
# the amount a player won, and the total wager are formatted as strings with two decimal
# places and stored as values in the dictionary)
        player_data['balance'] = "{:.2f}".format(self.balance)
        player_data['bet_size'] = "{:.2f}".format(self.bet_size)
#If the players last payout is zero, it is represented as "N/A" in the directionary
        player_data['last_payout'] = "{:.2f}".format(self.last_payout) if self.last_payout else "N/A"
        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        return player_data
# A new method "place_bet is created"
    def place_bet(self):
# a variable "bet" is define and represents a players initial bet size
        bet = self.bet_size
# a players new balance equals the initial balance minus the bet size 
        self.balance -= bet
# a players new total wager equals the initial total wager minus the bet size 
        self.total_wager += bet

#A new class called "Reel" is defined
class Reel:
#The method __init__ initializes the instance variables of the object "Reel"
    def __init__(self, pos):
#Symbols in the reel are stored by using "symbol_list" which is a "pygame.sprite.Group"
        self.symbol_list = pygame.sprite.Group()
# A list of symbols are randomly shuffled and truncated to a length of 5
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5] # Only matters when there are more than 5 symbols
# the variable self.reel_reel_is_spinning indicate whether the reel is crruently spinning
# Starting the game the reel is not spinning therefore it is set to "False"
        self.reel_is_spinning = False

        # Sounds
        # self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
        # self.stop_sound.set_volume(0.5)
        
#A for loop is created. It creates instances of the class "Symbol" for each symbol 
# in the "shuffled_keys" which is a list with the symbols
#  Each symbol is added to the symbol_list group with the corresponding position pos and index idx
#The position value is updated to 150 which shifts the vertically for each symbol
        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 150
            pos = tuple(pos)
# A new method called "animate" is created and takes a prarameter "delta_time"
    def animate(self, delta_time):
# The if statement checks if the reel is currently spinning
# If it is the case, the current delay_time and spin_time is substracted by delta_time *1000
# Furthermore, reel_is_stopping is set to False
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False
# The next if statement checks if the spin_time is smaller than zero. If so, 
# this means that the reel is stopping. Therefore, reel_is_stopping is set to True
            if self.spin_time < 0:
                reel_is_stopping = True

            # Stagger reel spin start animation
# The next if statement checks if the delay_time equals zero or if it is lower. 
            if self.delay_time <= 0:

                # Iterate through all 5 symbols in reel; truncate; add new random symbol on top of stack
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 50

 # If statement checks if the symbol's rect top attribute has reached 600
                    if symbol.rect.top == 600:
# If reel_is_stopping is True, it sets self.reel_is_spinning to False, indicating that the reel has stopped
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()

                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Spawn random symbol in place of the above
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -150), symbol_idx))
#A new code named "start_spin" is defined within the class which 
#takes the parameter "delay_time". 
#The variables within the method control the timing of the reel spin animation
    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
#The reel has started spinning
        self.reel_is_spinning = True

# A method called "reel_spin_result" is defined
    def reel_spin_result(self):
        # Get and return text representation of symbols in a given reel
        spin_symbols = []
# the reel_spin_result method iterated through the list "GAME_INDICES"
#The defined symbols are appended to the spin_symbols list. The list is then reversed
# and and returned
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1]

#A new class called "Symbol" is defined
class Symbol(pygame.sprite.Sprite):
# The method __init__ initializes the insatnce variable of the "Symbols"
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        # Friendly name
        self.sym_type = pathToFile.split('/')[3].split('.')[0]
#"pos" and "idx" values are assigned to the instance variables "self.pos" and "self.idx"
        self.pos = pos
        self.idx = idx
        #Loading image file specified with pathToFile using "pygame.image.load"
        self.image = pygame.image.load(pathToFile).convert_alpha()
        #this code results in the rectangle being assigned to self.rect after the 
        #topleft corner of the rectangle is set to the given position
        self.rect = self.image.get_rect(topleft = pos)
        #The left position of the rectangle is assigned to the variable self.x_val
        self.x_val = self.rect.left

        # Used for win animations
        self.size_x = 150 #size
        self.size_y = 150  #size
        self.alpha = 255 #transparency level of the symbol
        # "self.fade_out" and "self.fade_in" indicate that the symbols should not be fade out
        # or in during win animations 
        self.fade_out = False
        self.fade_in = False
    #A new method "update" is created to update 
    def update(self):
        # Slightly increases size of winning symbols the state of the symbols
        if self.fade_in:
            if self.size_x < 160:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        
        # Fades out non-winning symbols if the previuos condition is not met
        elif not self.fade_in and self.fade_out:
            #value of alpha (transparency) is decresed by seven if alpha is lower than 115
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)

# An new class called "UI" is defined and the object palyer is assigned to self.player
#
class UI:
    def __init__(self, player):
        self.player = player
        #self.display_surface represents the display surface where the UI will be drawn
        self.display_surface = pygame.display.get_surface()
        #The code attempts to load different fonts
        try:
            self.font, self.bet_font = pygame.font.SysFont(None, 30), pygame.font.SysFont(None, 30)
            self.small_font = pygame.font.SysFont(None, 15, italic=True)
            self.win_font = pygame.font.SysFont(None, 30)
        #If loads can't be loaded the message below will be printed and the program is terminated 
        except:
            print("Error loading font!")
            print(f"Currently, the UI_FONT variable is set to {UI_FONT}")
            print("Does the file exist?")
            quit()
        #The angle at which will be displayed is set
        self.win_text_angle = random.randint(-4, 4)
    # An new method called "display_info" is created through which player related
    #information are displayed on the screen 
    def display_info(self):
        player_data = self.player.get_data()

        # Surface for rendering the player's balance is created by display_info
        balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR, (0, 0, 0, 0))
        x, y = 20, self.display_surface.get_size()[1] - 15
        balance_rect = balance_surf.get_rect(bottomleft = (x, y))
        
        # Surface for instruction for playing is created by display_info
        instructions_play = self.small_font.render("Press space or enter to spin.", True, TEXT_COLOR, (0, 0, 0, 0))
        x, y = 20, self.display_surface.get_size()[1] - 15
        instructions_play_rect = instructions_play.get_rect(bottomleft = (x, y+10))

        # Surface for the bet size is created by display_info
        bet_surf = self.bet_font.render("Bet: $" + player_data['bet_size'], True, TEXT_COLOR, (0, 0, 0, 0))
        x = self.display_surface.get_size()[0] - 10
        bet_rect = bet_surf.get_rect(bottomright = (x, y))

        # Surface for instructions for adjusting the bet is created by display_info
        instructions_bet = self.small_font.render("Increase/Decrease with arrow keys.", True, TEXT_COLOR, (0, 0, 0, 0))
        x = self.display_surface.get_size()[0] - 10
        instructions_bet_rect = instructions_bet.get_rect(bottomright = (x, y+10))

        # Draw player data
        #Drawing rectangles on the "display_surface" using "pygame.draw.rect"
        #Color "False" means that the rectangle are transparent
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        pygame.draw.rect(self.display_surface, False, instructions_play_rect)
        pygame.draw.rect(self.display_surface, False, instructions_bet_rect)

        #the blit function is used isdraw the surface, "balance_surf", "bet_surf",
        # "instructions_play" and "instructions_bet"
        #Surfaces are drawn based on their corresponding rectangle position
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)
        self.display_surface.blit(instructions_play, instructions_play_rect)
        self.display_surface.blit(instructions_bet, instructions_bet_rect)

        # Print last win if applicable
        # The if statement checks if the player last_payout is not "None". If it is not "None"
        # then the player won when spinning last time
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            #A text with the winning amount is assigned to win_surf
            win_surf = self.win_font.render("WIN! $" + last_payout, True, TEXT_COLOR, None)
           # Rotation of the surface
           #Rectangle for rotated surface is obtained where "x1 is set to 400" and y is calculated 
           # based on the size of the display surface
            x1 = 400
            y1 = self.display_surface.get_size()[1] - 30
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center = (x1, y1))
            self.display_surface.blit(win_surf, win_rect)
    # The method "update" is used to update the surface. The new dimensions and positions are defined
    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 450, 800, 50))
        self.display_info()
#A new code called "Machine" is defined
class Machine:
    def __init__(self):
        #the display surface obtained from pygame.display.get_surface() is assigned 
        #self.dispaly_surface
        self.display_surface = pygame.display.get_surface()
        #Opening the file "wallet.json" and loading its content as a JSON object
        with open("wallet.json", "r") as wallet:
            wallet = json.load(wallet)
            #Assigning "money" of the JSON object to money
            money = wallet["money"]
        #The total machine balance is calculated by summing the money amount in the list of "money"
        #The amount is then assigned to "self.machine_balance"
        self.machine_balance = sum(money)
        self.reel_index = 0 #current index
        self.reel_list = {} #Directionary for storing the reel objects
        # Several aspects of the machine are controlled
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        # Results
        #The dictionary self.pre_result keeps track of the previous result
        # The dictionary self.spin_result keeps track of the current result
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        
        #initializing of reels, player, and user interface (UI)
        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

        # Import sounds
        # SAnd setting volumes for the different sounds that are being imported
        self.win_three = pygame.mixer.Sound('audio/win.wav')
        self.win_three.set_volume(0.6)
        self.win_four = pygame.mixer.Sound('audio/win.wav')
        self.win_four.set_volume(0.7)
        self.win_five = pygame.mixer.Sound('audio/win.wav')
        self.win_five.set_volume(0.8)
        
    # A new method "cooldown" is created for managing cooldown and the game state related to the function
    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()
       
            #checking if the palyer won after spinning, if so win data is assigned to 
            # self.win.data
            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                # Play the win sound
                self.play_win_sound(self.win_data)
                #Pay the player by calling self.pay_player(self.win_data, self.currPlayer)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                # Angle is randomly assigned to self.ui.win_text_angle
                self.ui.win_text_angle = random.randint(-4, 4)
                
    #  method input is responsible for handling user input
    # The state of all keys is stored in the "keys" variable
    def input(self):
        keys = pygame.key.get_pressed()

        # Checks for space key or enter key, ability to toggle spin, and balance to cover bet size
        if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size and self.currPlayer.bet_size>0:
            #checks if conditions are met then the actions below are performed:
            self.toggle_spinning()  # toggle the spinning  
            self.spin_time = pygame.time.get_ticks() #tracking the spinning time
            self.currPlayer.place_bet() #Deducting the bet amount from a players balance
            self.machine_balance += self.currPlayer.bet_size #Machine balance is increased by the bet amount
            self.currPlayer.last_payout = None #Indicating that there is no previous payout

        #Lines helps handling the input for increasing and decreasing the bet size
        if keys[pygame.K_UP] and self.can_toggle and self.currPlayer.balance > self.currPlayer.bet_size:
            #bet size is increased by 1 if the up arrow key is pressed and the 
            # the spinning can be toggled and the player's balance is greater than the current size
            self.currPlayer.bet_size += 1
            #delay of 200ms to avoid rapid key presses
            pygame.time.wait(200)
        if keys[pygame.K_DOWN] and self.can_toggle and self.currPlayer.bet_size >0:
            self.currPlayer.bet_size -= 1
            pygame.time.wait(200)



     #Method for animating the reels        
    def draw_reels(self, delta_time):
        #Iterating over each reel and calling animate() method and
        # passing delta_time as an argument
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)
            
#Method for creating and positioning the reels
    def spawn_reels(self):
        #checking if empty, if so: initializing variables x_topleft and y_topleft
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        # x_topleft and y_topleft are initialized based on while loop amd if statement
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (150 + X_OFFSET), y_topleft
            #initiating the Reel class with the current position
            # resulting reel object is added to self.reel_list
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft)) # Need to create reel class
            self.reel_index += 1
            
    # toggling the spinning state of the machine
    def toggle_spinning(self):
        #Checking if spinning can be toggled if so:
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks() #Setting current time
            self.spinning = not self.spinning #self.spinning" is updated
            self.can_toggle = False #Avoiding immediate toggling
 
            # for loop that iterates reel through "self.reel_list"
            for reel in self.reel_list:
                #"start_spin" method of each reel is called 
                self.reel_list[reel].start_spin(int(reel) * 200)
                #self.spin_sound.play()
                #No on going win animation
                self.win_animation_ongoing = False
    #Retrieving the result of each reel spin
    def get_result(self):
        # Interating over each reel and ssigning the result of calling
        # the method "reel_spin_result()" of each reel to respective key in "self.spin_result"
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        #returning self.spin_result
        return self.spin_result
    # checking  for winning combinations in the spin result.
    def check_wins(self, result):
        #Initializing empty list
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2: # Potential win if symbol appears more than twice
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]

                    # Check possible_win for a subsequence longer than 2 and add to hits
                    if len(longest_seq(possible_win)) > 2:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits
    #responsible for calculating and updating the player's balance based on the win data
    def pay_player(self, win_data, curr_player):
        #initializing multiplier and spin_payout
        multiplier = 0
        spin_payout = 0
        #  iterating over the values in win_data and adding the length of the subsequence (v[1]) 
        # to the multiplier for each winning combination.
        for v in win_data.values():
            multiplier += len(v[1])
        spin_payout = (multiplier * curr_player.bet_size) #Calculation of spin_payout
        curr_player.balance += spin_payout #Updating "curr_player.balance", "self.achine_balance"
        # "self.machine_balance", "curr_player.last_payout", "curr_player.total_won" based on "spin_payout"
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    # playing the win sounds based on the number of winning combinations.
    def play_win_sound(self, win_data):
        sum = 0
         # iterating over the values in win_data 
         # and adding the length of the subsequence (item[1]) to the sum for each winning combination.
        for item in win_data.values():
            sum += len(item[1])
        #Different song is played based on the value of sum
        if sum == 3: self.win_three.play()
        elif sum == 4: self.win_four.play()
        elif sum > 4: self.win_five.play()

    # animating the winning symbols with the method "win_animation"
    def win_animation(self):
        # Checking if win_animation is ongoing and win data is available
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                # They key "k" determine the animation row 
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                #The animationCols variable is assigned the 
                # value of v[1] (the columns of the winning symbols)
                animationCols = v[1]
                for reel in self.reel_list:
                    #If the reel is in the animationCols and animation is allowed 
                    # (self.can_animate), it sets the fade_in attribute of the corresponding 
                    # symbol in the third row (animationRow) to True.
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                   #for each symbol in the reel's symbol list, if the symbol's fade_in attribute is False, it sets the fade_out attribute to True.
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True

# Update method  for updating the game state
    def update(self, delta_time):
        self.cooldowns() #handling cooldown logic related to spinning and toggling.
        self.input() # handling player input, including spinning the machine and adjusting the bet size.
        self.draw_reels(delta_time) # Updating and animating the reels
        for reel in self.reel_list: #iterating over each reel in "self.reel_list"
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update() #updating the position and appearance of the symbols.
        self.ui.update()   # Updating the UI display (player balance, bet size, and instructions)
        self.win_animation() #animating the winning symbols if a win animation is ongoing.

        # Balance/payout debugger
        # debug_player_data = self.currPlayer.get_data()
        # machine_balance = "{:.2f}".format(self.machine_balance)
        # if self.currPlayer.last_payout:
        #     last_payout = "{:.2f}".format(self.currPlayer.last_payout)
        # else:
        #     last_payout = "N/A"
        # debug(f"Player balance: {debug_player_data['balance']} | Machine balance: {machine_balance} | Last payout: {last_payout}")

# Helper functions to detect wins

def flip_horizontal(result):
    # Flip results horizontally to keep them in a more readable list
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
    # 'Rotate' 90 degrees to get text representation of spin in order
    #initializing rows and cols variables to store the 
    # dimensions of horizontal_values using len(horizontal_values) and 
    # len(horizontal_values[0])
    rows, cols = len(horizontal_values), len(horizontal_values[0])
    hvals2 = [[""] * rows for _ in range(cols)]
    for x in range(rows):
        for y in range(cols):
            hvals2[y][rows - x - 1] = horizontal_values[x][y]
    hvals3 = [item[::-1] for item in hvals2]
    # The function returns hvals3, which 
    # represents the spin result with symbols in the correct order.
    return hvals3 
# longest_seq is used to find the longest sequential 
# subsequence in a list. Taking hit as a parameter, which is a list of indices.
def longest_seq(hit):
    subSeqLength, longest = 1, 1
    start, end = 0, 0
    #Iterating over the indices in hit except for the last one using a for loop.
    for i in range(len(hit) - 1):
        # Check to see if indices in hit parameter are sequential
        if hit[i] == hit[i + 1] - 1:
            subSeqLength += 1
            if subSeqLength > longest:
                longest = subSeqLength
                start = i + 2 - subSeqLength
                end = i + 2
        else:
            subSeqLength = 1
    return hit[start:end] # Returning the subsequence from hit using the start and end indices.

# This class represents the game itself
class Game:
    def __init__(self):

        # The codes below make the general setup of the game
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Slot Machine')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        self.machine = Machine()
        self.delta_time = 0

        # loading and playing the main sound track using Pygame's
        # mixer module.The sound volume is set to 0.2, and 
        # the sound is played in an infinite loop.
        main_sound = pygame.mixer.Sound('audio/track.mp3')
        main_sound.set_volume(0.2)
        main_sound.play(loops = -1)
    # The run() method is the main game loop, running forever until the game is exited.
    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # update money to be used in shop etc. by retrieving  
                    #  the new balance from the Machine instance and storing it in the file. 
                    with open("wallet.json", "w") as jsonFile: 
                        money = []
                        new_balance = self.machine.currPlayer.get_data()
                        money.append(int(round(float(new_balance["balance"]))))
                        wallet = {}
                        wallet["money"] = money
                        json.dump(wallet, jsonFile)

                    pygame.quit()
                    sys.exit()

            # Time variables, the lines calulate the time difference between the current tick
            # the previous tick. Through this the elapsed time since the last frame update is obtained
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            
           

            pygame.display.update() #updating the display
            self.screen.blit(self.bg_image, (0, 0))  # blitting images onto the screen, 
            self.machine.update(self.delta_time) # updating the game state
            self.screen.blit(self.grid_image, (0, 0)) # blits the grid image onto the screen at the position (0, 0).
            self.clock.tick(FPS) #controlling the frame rate.

#checking if the module is being run as the main program
#if so the game loop starts
if __name__ == '__main__':
    game = Game()
    game.run()
