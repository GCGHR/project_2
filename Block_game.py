import pygame
import random

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арканоид")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Игровые объекты
block_width = 60
block_height = 20
block_padding = 5
paddle_width = 100
paddle_height = 15
ball_radius = 10

# Частота обновления экрана
clock = pygame.time.Clock()
FPS = 60

# Начальные параметры игры
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 10
paddle_dx = 0

ball_x = screen_width // 2
ball_y = paddle_y - ball_radius - 1
ball_dx = 3 * random.choice([1, -1])
ball_dy = -3

# Список блоков
blocks = []
for row in range(5):
    for col in range(screen_width // (block_width + block_padding)):
        block = pygame.Rect(col * (block_width + block_padding), row *
                            (block_height + block_padding), block_width, block_height)
        blocks.append(block)

# Функция для отрисовки блоков


def draw_blocks():
    for block in blocks:
        pygame.draw.rect(screen, BLUE, block)


# Главный игровой цикл
running = True
while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_dx = -5
    elif keys[pygame.K_RIGHT]:
        paddle_dx = 5
    else:
        paddle_dx = 0

    # Двигаем платформу
    paddle_x += paddle_dx
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > screen_width - paddle_width:
        paddle_x = screen_width - paddle_width

    # Двигаем мяч
    ball_x += ball_dx
    ball_y += ball_dy

    # Столкновение с границами экрана
    if ball_x <= 0 or ball_x >= screen_width - ball_radius * 2:
        ball_dx = -ball_dx
    if ball_y <= 0:
        ball_dy = -ball_dy

    # Столкновение с платформой
    if paddle_y <= ball_y + ball_radius * 2 <= paddle_y + paddle_height and paddle_x <= ball_x <= paddle_x + paddle_width:
        ball_dy = -ball_dy

    # Столкновение с блоками
    ball_rect = pygame.Rect(ball_x, ball_y, ball_radius * 2, ball_radius * 2)
    for block in blocks[:]:
        if ball_rect.colliderect(block):
            ball_dy = -ball_dy
            blocks.remove(block)

    # Отображаем объекты
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y,
                     paddle_width, paddle_height))
    pygame.draw.circle(screen, RED, (ball_x + ball_radius,
                       ball_y + ball_radius), ball_radius)
    draw_blocks()

    # Обновляем экран
    pygame.display.update()

    # Проверка на окончание игры
    if not blocks:
        print("Победа! Все блоки разрушены.")
        running = False

    # Частота обновления экрана
    clock.tick(FPS)

# Закрытие игры
pygame.quit()
