import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ну, погоди!')

clock = pygame.time.Clock()

# Загрузите изображения и звуки
wolf_image = pygame.image.load('wolf.png')  # Замените на ваш файл изображения
egg_image = pygame.image.load('egg.png')  # Замените на ваш файл изображения

font = pygame.font.Font(None, 36)

class Wolf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = wolf_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.position = 0  # 0: left-up, 1: left-down, 2: right-up, 3: right-down

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            if keys[pygame.K_UP]:
                self.position = 0
            elif keys[pygame.K_DOWN]:
                self.position = 1
        elif keys[pygame.K_RIGHT]:
            if keys[pygame.K_UP]:
                self.position = 2
            elif keys[pygame.K_DOWN]:
                self.position = 3

        # Обновить позицию волка на экране
        if self.position == 0:
            self.rect.topleft = (50, 50)
        elif self.position == 1:
            self.rect.bottomleft = (50, SCREEN_HEIGHT - 50)
        elif self.position == 2:
            self.rect.topright = (SCREEN_WIDTH - 50, 50)
        elif self.position == 3:
            self.rect.bottomright = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = egg_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 5
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

wolf = Wolf()
all_sprites = pygame.sprite.Group()
all_sprites.add(wolf)
eggs = pygame.sprite.Group()

# Переменные для счета и жизней
score = 0
lives = 3

# Функция для создания новых яиц
def create_egg():
    x_positions = [70, 70, SCREEN_WIDTH - 70, SCREEN_WIDTH - 70]
    y_positions = [70, SCREEN_HEIGHT - 70, 70, SCREEN_HEIGHT - 70]
    position = random.randint(0, 3)
    egg = Egg(x_positions[position], y_positions[position])
    eggs.add(egg)
    all_sprites.add(egg)

# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    wolf.update(keys)

    # Создание новых яиц
    if len(eggs) < 10 and random.randint(1, 60) == 1:
        create_egg()

    # Обновление спрайтов
    all_sprites.update(keys)

    # Проверка столкновений
    for egg in eggs:
        if pygame.sprite.collide_rect(wolf, egg):
            egg.kill()
            score += 1

    # Проверка, если яйцо достигло нижней части экрана
    for egg in eggs:
        if egg.rect.y > SCREEN_HEIGHT:
            egg.kill()
            lives -= 1
            if lives == 0:
                pygame.quit()
                sys.exit()

    # Отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Отображение счета и жизней
    score_text = font.render(f'Score: {score}', True, BLACK)
    lives_text = font.render(f'Lives: {lives}', True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)
