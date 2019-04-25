import os
import sys
import pygame

level_name = input()
FPS = 60
size = WIDTH, HEIGHT = 630, 420
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                print
            elif level[y][x] == '@':
                Tile('empty', x, y)
                hero_x, hero_y = x, y

    return Player(hero_x, hero_y), x, y


def load_level(filename):
    filename = "data/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (70, 70))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (50, 70))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y)

    def update(self, x=0, y=0):
        self.rect = self.rect.move(x, y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


level = load_level(level_name)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
camera = Camera()
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')
start_screen()
tile_width = tile_height = 70
player, pos_x, pos_y = generate_level(level)
pygame.init()
running = True


while running:
    screen.fill(pygame.Color("white"))
    for event in pygame.event.get():

        key = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            running = False

        if key[pygame.K_LEFT]:
            player.update(-tile_height, 0)

        if key[pygame.K_RIGHT]:
            player.update(tile_height, 0)

        if key[pygame.K_DOWN]:
            player.update(0, tile_height)

        if key[pygame.K_UP]:
            player.update(0, -tile_height)

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
