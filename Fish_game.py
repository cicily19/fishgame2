import pygame
import random
import sys

# Initialize pygame and constants
pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)

# Game settings
fish_speed = 7
bubble_speed = 3
bubble_spawn_rate = 30  # Frames between new bubbles

# Initialize screen and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Bubble Shooter")
font = pygame.font.SysFont(None, 36)

# Game variables
score = 0
game_over = False

# Fish setup
fish_color = (0, 100, 255)
fish_width, fish_height = 60, 30
fish_rect = pygame.Rect(WIDTH // 10, HEIGHT // 2 - fish_height // 2, fish_width, fish_height)

# Bubble and particle lists
bubbles = []
particles = []  # For ocean effect particles

# Bullet setup
bullet_image = pygame.Surface((10, 5))
bullet_image.fill(RED)
bullets = []

# Classes
class Bubble:
    def _init_(self, bouncing=True):  # Corrected constructor method
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (15, 15), 15)
        self.rect = self.image.get_rect(center=(WIDTH, random.randint(0, HEIGHT)))
        self.bouncing = bouncing
        if self.bouncing:
            # Bouncing bubbles move diagonally leftward
            self.speed_x = -bubble_speed
            self.speed_y = random.choice([-bubble_speed, bubble_speed])
        else:
            self.speed_x = -bubble_speed
            self.speed_y = 0

    def move(self):  # Bubble movement method
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y if self.bouncing else 0
        # Bounce off top and bottom edges
        if self.bouncing:
            if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
                self.speed_y *= -1

    def draw(self):  # New draw method to render the bubble on the screen
        screen.blit(self.image, self.rect)


class Bullet:
    def _init_(self, x, y):
        self.rect = bullet_image.get_rect(center=(x, y))

    def move(self):
        self.rect.x += 10  # Bullet speed

    def draw(self):
        screen.blit(bullet_image, self.rect)


class Particle:
    """Small particles moving to simulate an ocean effect."""
    def _init_(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.size = random.randint(1, 3)

    def move(self):
        self.y += self.speed_y
        if self.y < 0 or self.y > HEIGHT:
            self.y = random.randint(0, HEIGHT)  # Reset position

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)


# Functions
def move_fish(keys):
    if keys[pygame.K_UP] and fish_rect.top > 0:
        fish_rect.y -= fish_speed
    if keys[pygame.K_DOWN] and fish_rect.bottom < HEIGHT:
        fish_rect.y += fish_speed


def draw_fish():
    pygame.draw.ellipse(screen, fish_color, fish_rect)  # Fish body
    pygame.draw.polygon(screen, WHITE, [
        (fish_rect.left, fish_rect.centery),
        (fish_rect.left - 15, fish_rect.centery - 10),
        (fish_rect.left - 15, fish_rect.centery + 10)
    ])  # Fish tail
    pygame.draw.circle(screen, WHITE, (fish_rect.right - 10, fish_rect.centery - 5), 3)  # Fish eye


def draw_ocean_background():
    """Draws a gradient background and moving particles for an ocean effect."""
    for i in range(HEIGHT):
        color = (0, 0, int(50 + (i / HEIGHT) * 100))  # Gradient blue
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))
    # Draw particles
    for particle in particles:
        particle.move()
        particle.draw()


def spawn_bubble():
    # Randomly decide if a bubble is bouncing or moving straight left
    bouncing = random.choice([True, False])
    if random.randint(0, bubble_spawn_rate) == 0:
        bubbles.append(Bubble(bouncing))


def move_bubbles():
    global bubbles, game_over
    for bubble in bubbles:
        bubble.move()
        if bubble.rect.left <= 0 and not bubble.bouncing:
            game_over = True  # End game if a non-bouncing bubble reaches the left side
    bubbles = [bubble for bubble in bubbles if bubble.rect.x > 0]  # Remove bubbles out of screen


def move_bullets():
    global bullets, score
    for bullet in bullets:
        bullet.move()
        for bubble in bubbles[:]:
            if bullet.rect.colliderect(bubble.rect):
                bubbles.remove(bubble)
                bullets.remove(bullet)
                score += 1
                break
    bullets = [bullet for bullet in bullets if bullet.rect.x < WIDTH]


def draw_elements():
    draw_ocean_background()
    draw_fish()
    for bubble in bubbles:
        bubble.draw()
    for bullet in bullets:
        bullet.draw()
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def display_game_over():
    game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))


# Main game loop
def main():
    global game_over
    clock = pygame.time.Clock()

    # Initialize particles for the ocean background
    for _ in range(50):
        particles.append(Particle())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    # Shoot a bullet from the fish's position
                    bullets.append(Bullet(fish_rect.right, fish_rect.centery))

        if not game_over:
            keys = pygame.key.get_pressed()
            move_fish(keys)
            spawn_bubble()
            move_bubbles()
            move_bullets()
            draw_elements()
        else:
            display_game_over()

        pygame.display.flip()
        clock.tick(30)

if _name_ == "_main_":
    main()