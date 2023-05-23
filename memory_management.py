import pygame, random, os, json
from PIL import Image

class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('_')[0]


        self.original_image = self.load_image('graphic/memory/content_management/' + filename)

        self.back_image = pygame.image.load('graphic/memory/0_unisg.png').convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (80, 80))

        self.image = self.back_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shown = False

    def load_image(self, path):
        image = Image.open(path)
        image = image.convert("RGBA")  # Konvertieren Sie das Bild in das richtige Format (RGBA)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)

    def update(self):
        self.image = self.original_image if self.shown else self.back_image

    def show(self):
        self.shown = True

    def hide(self):
        self.shown = False


class Game():
    def __init__(self):
        with open("wallet.json", "r") as wallet:
            wallet = json.load(wallet)
            self.score = sum(wallet["money"])

        self.content_font = pygame.font.Font('graphic/memory/fonts/font.ttf', 12)

        self.level = 1
        self.level_complete = False

        # graphics
        self.all_graphics = [f for f in os.listdir('graphic/memory/content_management') if os.path.isfile(os.path.join('graphic/memory/content_management', f)) and f.endswith(('.png', '.jpg', '.jpeg'))]

        # sort list with all possible memory cards by number 
        def custom_sort_key(file_name):
            # Extract the numeric part of the filename
            file_number = int(file_name.split('_')[0])
            # Extract the suffix (question or answer) of the filename
            file_suffix = file_name.split('_')[1]
            # Multiply the number by 2 for "question" files and add 1 for "answer" files
            if file_suffix == 'question.png':
                return file_number * 2
            else:
                return file_number * 2 + 1
        # finally sorting list of all memory cards 
        self.all_graphics = sorted(self.all_graphics, key=custom_sort_key)



        self.img_width, self.img_height = (80, 80)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 600

        self.tiles_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level(self.level)

        # initialize image
        self.background_image = pygame.image.load('graphic/memory/square.jpg').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (WINDOW_HEIGHT, WINDOW_WIDTH))

    def increase_score(self):
        self.score += 5

    def decrease_score(self):
        self.score -= 5
        if self.score < 0:
            self.score = 0

    def resize_image(self, image, size):
        pil_image = Image.fromarray(image)
        resized_image = pil_image.resize(size)
        return pygame.surfarray.array3d(resized_image)

    def update(self, event_list):
        self.user_input(event_list)
        self.draw()
        self.check_level_complete(event_list)

    def check_level_complete(self, event_list):
        if not self.block_game:
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos) and not tile.shown:
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                    # self.decrease_score()  # Decrease score if wrong card chosen
                                else:
                                    self.flipped = []
                                    self.increase_score()  # Erhöhe den Score

                                    
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False

                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []

    def generate_level(self, level):
        self.graphics = self.select_random_graphics(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.graphics)

    def generate_tileset(self, graphics):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        self.tiles_group.empty()

        for i in range(len(graphics)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(graphics[i], x, y)
            self.tiles_group.add(tile)

    def select_random_graphics(self, level): 
        graphics = []
        graphics_filter = random.sample(range(0,24,2), (self.level + self.level + 2))
        for i in graphics_filter:
            graphics.append(self.all_graphics[i])
            graphics.append(self.all_graphics[i+1])
        random.shuffle(graphics)
        return graphics



    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 5:
                        self.level = 1
                    self.generate_level(self.level)

    def draw(self):
        screen.fill(BLACK)

        # fonts
        title_font = pygame.font.Font('graphic/memory/fonts/font.ttf', 20)
        content_font = pygame.font.Font('graphic/memory/fonts/font.ttf', 12)
        default_font = pygame.font.SysFont(None, 20)
        default_font2 = pygame.font.SysFont(None, 30)


        # draw background image
        screen.blit(self.background_image, (0, 0))

        score_text = default_font.render("Current balance: $"+ str(self.score), True, BLACK)
        score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 30, 20))
        screen.blit(score_text, score_rect)



        # text
        title_text = title_font.render('Memory Game', True, BLACK)
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Level ' + str(self.level), True, BLACK)
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 40))

        info_text = content_font.render('Find the matching answer to the questions.', True, BLACK)
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80))

        if not self.level == 4:
            next_text = default_font2.render('Level complete! Press space for next level.', True, WHITE)
        else:
            next_text = default_font2.render('Congrats! You Won! Press space to play again.', True, WHITE)
        next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete:
            screen.blit(next_text, next_rect)

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Memory Game')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

game = Game()

running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            with open("wallet.json", "w") as jsonFile: 
                money = []
                new_balance = game.score
                money.append(int(round(float(new_balance))))
                wallet = {}
                wallet["money"] = money
                json.dump(wallet, jsonFile)

            running = False

    game.update(event_list)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
