import ctypes, pygame, sys, random
# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

# Display settings
DEFAULT_IMAGE_SIZE = (150, 150)
FPS = 120
HEIGHT = 500
WIDTH = 800
START_X, START_Y = 0, -150
X_OFFSET, Y_OFFSET = 10, 0

# Images
BG_IMAGE_PATH = 'graphic/slot/bg.png'
GRID_IMAGE_PATH = 'graphic/slot/gridline.png'
GAME_INDICES = [1, 2, 3] # 0 and 4 are outside of play area
SYM_PATH = 'graphic/slot/symbols'

# Text
TEXT_COLOR = 'White'


# 5 Symbols for demo
# symbols = {
#     'diamond': f"{SYM_PATH}/0_diamond.png", 
#     'floppy': f"{SYM_PATH}/0_floppy.png",
#     'hourglass': f"{SYM_PATH}/0_hourglass.png",
#     'seven': f"{SYM_PATH}/0_seven.png",
#     'telephone': f"{SYM_PATH}/0_telephone.png"
# }

# 4 Symbols for more wins
symbols = {
    'diamond': f"{SYM_PATH}/0_diamond.png", 
    'floppy': f"{SYM_PATH}/0_floppy.png",
    'hourglass': f"{SYM_PATH}/0_hourglass.png",
    'hourglass2': f"{SYM_PATH}/0_hourglass.png",
    'telephone': f"{SYM_PATH}/0_telephone.png"
}




class Player():
    def __init__(self):
        self.balance = 1000.00
        self.bet_size = 10.00
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00

    def get_data(self):
        player_data = {}
        player_data['balance'] = "{:.2f}".format(self.balance)
        player_data['bet_size'] = "{:.2f}".format(self.bet_size)
        player_data['last_payout'] = "{:.2f}".format(self.last_payout) if self.last_payout else "N/A"
        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        return player_data

    def place_bet(self):
        bet = self.bet_size
        self.balance -= bet
        self.total_wager += bet


class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5] # Only matters when there are more than 5 symbols

        self.reel_is_spinning = False

        # Sounds
        # self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
        # self.stop_sound.set_volume(0.5)

        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 150
            pos = tuple(pos)
            print(self.shuffled_keys)
    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            # Stagger reel spin start animation
            if self.delay_time <= 0:

                # Iterate through all 5 symbols in reel; truncate; add new random symbol on top of stack
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 50

                    # Correct spacing is dependent on the above addition eventually hitting 1200
                    if symbol.rect.top == 600:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()

                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Spawn random symbol in place of the above
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -150), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        # Get and return text representation of symbols in a given reel
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1]

class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        # Friendly name
        self.sym_type = pathToFile.split('/')[3].split('.')[0]

        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(pathToFile).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.x_val = self.rect.left

        # Used for win animations
        self.size_x = 150
        self.size_y = 150
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        # Slightly increases size of winning symbols
        if self.fade_in:
            if self.size_x < 160:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
        
        # Fades out non-winning symbols
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)


class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        try:
            self.font, self.bet_font = pygame.font.SysFont(None, 30), pygame.font.SysFont(None, 30)
            self.win_font = pygame.font.SysFont(None, 30)
        except:
            print("Error loading font!")
            print(f"Currently, the UI_FONT variable is set to {UI_FONT}")
            print("Does the file exist?")
            quit()
        self.win_text_angle = random.randint(-4, 4)

    def display_info(self):
        player_data = self.player.get_data()

        # Balance and bet size
        balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR, None)
        x, y = 20, self.display_surface.get_size()[1] - 15
        balance_rect = balance_surf.get_rect(bottomleft = (x, y))

        bet_surf = self.bet_font.render("Wager: $" + player_data['bet_size'], True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 10
        bet_rect = bet_surf.get_rect(bottomright = (x, y))

        # Draw player data
        pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)

        # Print last win if applicable
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! $" + last_payout, True, TEXT_COLOR, None)
            x1 = 400
            y1 = self.display_surface.get_size()[1] - 30
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center = (x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 450, 800, 50))
        self.display_info()

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        # Results
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

        # Import sounds
        # self.spin_sound = pygame.mixer.Sound('audio/spinclip.mp3')
        # self.spin_sound.set_volume(0.15)
        # self.win_three = pygame.mixer.Sound('audio/winthree.wav')
        # self.win_three.set_volume(0.6)
        # self.win_four = pygame.mixer.Sound('audio/winfour.wav')
        # self.win_four.set_volume(0.7)
        # self.win_five = pygame.mixer.Sound('audio/winfive.wav')
        # self.win_five.set_volume(0.8)

    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                # Play the win sound
                # self.play_win_sound(self.win_data)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

    def input(self):
        keys = pygame.key.get_pressed()

        # Checks for space key, ability to toggle spin, and balance to cover bet size
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None
            
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (150 + X_OFFSET), y_topleft
            
            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft)) # Need to create reel class
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                # self.spin_sound.play()
                self.win_animation_ongoing = False

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()
        return self.spin_result

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2: # Potential win
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]

                    # Check possible_win for a subsequence longer than 2 and add to hits
                    if len(longest_seq(possible_win)) > 2:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits

    def pay_player(self, win_data, curr_player):
        multiplier = 0
        spin_payout = 0
        for v in win_data.values():
            multiplier += len(v[1])
        spin_payout = (multiplier * curr_player.bet_size)
        curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    # You need to provide sounds and load them in the Machine init function for this to work!
    def play_win_sound(self, win_data):
        sum = 0
        for item in win_data.values():
            sum += len(item[1])
        if sum == 3: self.win_three.play()
        elif sum == 4: self.win_four.play()
        elif sum > 4: self.win_five.play()

    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()

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
    rows, cols = len(horizontal_values), len(horizontal_values[0])
    hvals2 = [[""] * rows for _ in range(cols)]
    for x in range(rows):
        for y in range(cols):
            hvals2[y][rows - x - 1] = horizontal_values[x][y]
    hvals3 = [item[::-1] for item in hvals2]
    return hvals3

def longest_seq(hit):
    subSeqLength, longest = 1, 1
    start, end = 0, 0
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
    return hit[start:end]

class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Slot Machine Demo')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        self.machine = Machine()
        self.delta_time = 0

        # Sound
        main_sound = pygame.mixer.Sound('audio/track.mp3')
        #main_sound.play(loops = -1)

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Time variables
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()

            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(self.delta_time)
            self.screen.blit(self.grid_image, (0, 0))
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
