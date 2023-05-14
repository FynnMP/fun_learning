import pygame, random, os
from PIL import Image

class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()

        self.name = filename.split('.')[0]


        self.original_image = self.load_image('graphic/Memory/Aliens/' + filename)

        self.back_image = pygame.image.load('graphic/Memory/Unknown.png').convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (128, 128))

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
        self.score = 0
        self.content_font = pygame.font.Font('Memory/fonts/Little Alien.ttf', 24)

        self.level = 1
        self.level_complete = False

        # aliens
        self.all_aliens = [f for f in os.listdir('graphic/Memory/Aliens') if os.path.isfile(os.path.join('graphic/Memory/Aliens', f)) and f.endswith(('.png', '.jpg', '.jpeg'))]


        self.img_width, self.img_height = (128, 128)
        self.padding = 20
        self.margin_top = 160
        self.cols = 4
        self.rows = 2
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()

        # flipping & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate first level
        self.generate_level(self.level)

        # initialize image
        self.background_image = pygame.image.load('graphic/Memory/Casino_Memory.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (1400, 1000))

        # initialize music
        self.is_music_playing = True
        self.sound_on = pygame.image.load('graphic/Memory/speaker.png').convert_alpha()
        self.sound_off = pygame.image.load('graphic/Memory/mute.png').convert_alpha()
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright=(WINDOW_WIDTH - 10, 10))

        # load music
        pygame.mixer.music.load('audio/brightside.mp3')
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play()

    def increase_score(self):
        self.score += 10

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
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                    self.decrease_score()  # Verringere den Score
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.shown:
                                            self.level_complete = True
                                            self.increase_score()  # Erhöhe den Score
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
        self.aliens = self.select_random_aliens(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        self.cols = 4
        self.generate_tileset(self.aliens)

    def generate_tileset(self, aliens):
        self.cols = self.rows = self.cols if self.cols >= self.rows else self.rows

        TILES_WIDTH = (self.img_width * self.cols + self.padding * 3)
        LEFT_MARGIN = RIGHT_MARGIN = (self.width - TILES_WIDTH) // 2
        self.tiles_group.empty()

        for i in range(len(aliens)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.margin_top + (i // self.rows * (self.img_height + self.padding))
            tile = Tile(aliens[i], x, y)
            self.tiles_group.add(tile)

    def select_random_aliens(self, level):
        aliens = random.sample(self.all_aliens, (self.level + self.level + 2))
        aliens_copy = aliens.copy()
        aliens.extend(aliens_copy)
        random.shuffle(aliens)
        return aliens

    def user_input(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 6:
                        self.level = 1
                    self.generate_level(self.level)

    def draw(self):
        screen.fill(BLACK)

        # draw background image
        screen.blit(self.background_image, (0, 0))

        score_text = self.content_font.render('Gewinn CHF: ' + str(self.score), True, WHITE)
        score_rect = score_text.get_rect(midtop=(WINDOW_WIDTH // 3, 100))
        screen.blit(score_text, score_rect)

        # fonts
        title_font = pygame.font.Font('Memory/fonts/Little Alien.ttf', 44)
        content_font = pygame.font.Font('Memory/fonts/Little Alien.ttf', 24)

        # text
        title_text = title_font.render('Memory Game', True, WHITE)
        title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))

        level_text = content_font.render('Level ' + str(self.level), True, WHITE)
        level_rect = level_text.get_rect(midtop=(WINDOW_WIDTH // 2, 80))

        info_text = content_font.render('Find 2 of each', True, WHITE)
        info_rect = info_text.get_rect(midtop=(WINDOW_WIDTH // 2, 120))

        if not self.level == 5:
            next_text = content_font.render('Level complete. Press Space for next level', True, WHITE)
        else:
            next_text = content_font.render('Congrats. You Won. Press Space to play again', True, WHITE)
        next_rect = next_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))

        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH - 90, 0, 100, 50))
        screen.blit(self.music_toggle, self.music_toggle_rect)

        # draw tileset
        self.tiles_group.draw(screen)
        self.tiles_group.update()

        if self.level_complete:
            screen.blit(next_text, next_rect)

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 860
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
            running = False

    game.update(event_list)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
