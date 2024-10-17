import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Simulation")

# Colors
COLOR_BACKGROUND = (35, 37, 74)
COLOR_MOUTH = (234, 158, 240)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = 2
        self.size = 20
        self.view_angle = math.pi / 2  # 90 degrees view angle
        self.view_distance = self.size * 2
        self.is_accelerating = False

    def rotate(self, angle):
        self.angle += angle

    def accelerate(self):
        self.speed += 0.1
        if self.speed > 5:
            self.speed = 5
        self.is_accelerating = True

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # Wrap around screen edges
        self.x %= WIDTH
        self.y %= HEIGHT
        
        # Reset acceleration flag
        self.is_accelerating = False

    def draw(self, screen, show_view):
        # Draw body (triangle)
        points = [
            (self.x + self.size * math.cos(self.angle), self.y + self.size * math.sin(self.angle)),
            (self.x + self.size * math.cos(self.angle + 2.5), self.y + self.size * math.sin(self.angle + 2.5)),
            (self.x + self.size * math.cos(self.angle - 2.5), self.y + self.size * math.sin(self.angle - 2.5))
        ]
        pygame.draw.polygon(screen, WHITE, points)

        # Draw eye
        eye_x = self.x + (self.size * 0.3) * math.cos(self.angle)
        eye_y = self.y + (self.size * 0.3) * math.sin(self.angle)
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(eye_y)), 3)

        # Draw mouth
        mouth_x = self.x + self.size * math.cos(self.angle)
        mouth_y = self.y + self.size * math.sin(self.angle)
        pygame.draw.circle(screen, COLOR_MOUTH, (int(mouth_x), int(mouth_y)), 5)

        # Draw acceleration indicator
        if self.is_accelerating:
            back_x = self.x - self.size * 0.7 * math.cos(self.angle)
            back_y = self.y - self.size * 0.7 * math.sin(self.angle)
            pygame.draw.circle(screen, BLUE, (int(back_x), int(back_y)), 3)

        # Draw field of view
        if show_view:
            start_angle = self.angle - self.view_angle / 2
            end_angle = self.angle + self.view_angle / 2
            pygame.draw.arc(screen, GREEN, 
                            (self.x - self.view_distance, self.y - self.view_distance, 
                             self.view_distance * 2, self.view_distance * 2),
                            -end_angle, -start_angle, 1)

    def draw_food_line(self, screen, food):
        mouth_x = self.x + self.size * math.cos(self.angle)
        mouth_y = self.y + self.size * math.sin(self.angle)
        pygame.draw.line(screen, WHITE, (int(mouth_x), int(mouth_y)), (food.x, food.y), 1)

# Food class
class Food:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 3)

# Toggle button class
class ToggleButton:
    def __init__(self, x, y, width, height, text, initial_state=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.state = initial_state
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        color = GREEN if self.state else (150, 150, 150)
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                return True
        return False

# Create birds and food
birds = [Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(10)]
foods = [Food() for _ in range(20)]

# Create toggle buttons
show_view_button = ToggleButton(10, 10, 100, 30, "View")
show_lines_button = ToggleButton(120, 10, 100, 30, "Lines")

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        show_view_button.handle_event(event)
        show_lines_button.handle_event(event)

    # Update birds
    for bird in birds:
        bird.rotate(random.uniform(-0.1, 0.1))
        if random.random() < 0.1:
            bird.accelerate()
        bird.move()

        # Check for collision with food
        for food in foods[:]:
            distance = math.hypot(bird.x - food.x, bird.y - food.y)
            if distance < bird.size:
                foods.remove(food)
                foods.append(Food())

    # Clear the screen
    screen.fill(COLOR_BACKGROUND)

    # Draw food and birds
    for food in foods:
        food.draw(screen)
    for bird in birds:
        bird.draw(screen, show_view_button.state)
        # Draw lines to nearby food
        if show_lines_button.state:
            for food in foods:
                distance = math.hypot(bird.x - food.x, bird.y - food.y)
                if distance < bird.view_distance:
                    bird.draw_food_line(screen, food)

    # Draw toggle buttons
    show_view_button.draw(screen)
    show_lines_button.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()