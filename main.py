import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Основные параметры окна и игры
WIDTH, HEIGHT = 1200, 693
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройки объектов
EGG_WIDTH, EGG_HEIGHT = 40, 50
WOLF_WIDTH, WOLF_HEIGHT = 160, 200
EGG_SPEED = 5
WOLF_SPEED = 30
NEW_EGG_INTERVAL = 500  # Миллисекунды


# Загрузка изображений
def load_image(name, width, height):
    return pygame.transform.scale(pygame.image.load(name), (width, height))


# Класс Egg
class Egg:
    def __init__(self, x, y):
        self.image = load_image("egg.png", EGG_WIDTH, EGG_HEIGHT)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += EGG_SPEED
        if self.rect.y > HEIGHT-200:
            return False
        return True

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Класс Wolf
class Wolf:
    def __init__(self, x, y):
        self.image = load_image("wolf.png", WOLF_WIDTH, WOLF_HEIGHT)
        self.rect = self.image.get_rect(midbottom=(x, y))

    def move(self, direction):
        if direction == 'left' and self.rect.x > 300:
            self.rect.x -= WOLF_SPEED
        elif direction == 'right' and self.rect.x < WIDTH - 300 - WOLF_WIDTH:
            self.rect.x += WOLF_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Класс Game
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.background = load_image("background.jpg", WIDTH, HEIGHT)
        self.wolf = Wolf(WIDTH // 2, HEIGHT - 150)
        self.eggs = []
        self.last_egg_time = pygame.time.get_ticks()
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Управление Волком
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.wolf.move('left')
            if keys[pygame.K_RIGHT]:
                self.wolf.move('right')

            # Добавление нового яйца
            current_time = pygame.time.get_ticks()
            if current_time - self.last_egg_time > NEW_EGG_INTERVAL:
                self.add_egg()
                self.last_egg_time = current_time

            # Обновление и отрисовка яиц
            self.update_eggs()

            # Отрисовка
            self.draw()

            self.clock.tick(FPS)

    def add_egg(self):
        x = random.randint(300, WIDTH - 300 - EGG_WIDTH)
        self.eggs.append(Egg(x, 100))

    def update_eggs(self):
        for egg in self.eggs[:]:
            if not egg.update():
                self.eggs.remove(egg)
                continue
            if self.wolf.rect.colliderect(egg.rect):
                self.score += 1
                self.eggs.remove(egg)

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.background, (0, 0))
        for egg in self.eggs:
            egg.draw(self.screen)
        self.wolf.draw(self.screen)
        self.draw_text(f'Score: {self.score}', 550, 150)
        pygame.display.flip()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    game = Game()
    game.run()
