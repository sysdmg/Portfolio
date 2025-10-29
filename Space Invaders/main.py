import pygame
import random
import sys
from pygame import mixer

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
PLAYER_SIZE = 50
ALIEN_SIZE = 40
BULLET_SIZE = 5
PLAYER_SPEED = 5
ALIEN_SPEED = 2
BULLET_SPEED = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        if direction == 'right' and self.x < WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x
        
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

class Alien:
    def __init__(self, x, y):
        self.width = ALIEN_SIZE
        self.height = ALIEN_SIZE
        self.x = x
        self.y = y
        self.speed = ALIEN_SPEED
        self.direction = 1  # 1 for right, -1 for left
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def move(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

class Bullet:
    def __init__(self, x, y):
        self.width = BULLET_SIZE
        self.height = BULLET_SIZE * 3
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def move(self):
        self.y -= self.speed
        self.rect.y = self.y
        
    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

class Game:
    def __init__(self):
        self.player = Player()
        self.aliens = []
        self.bullets = []
        self.score = 0
        self.game_over = False
        self.create_aliens()
        
    def create_aliens(self):
        for row in range(5):
            for col in range(10):
                x = col * (ALIEN_SIZE + 20) + 50
                y = row * (ALIEN_SIZE + 20) + 50
                self.aliens.append(Alien(x, y))
                
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and not self.game_over:
                if event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(
                        self.player.x + self.player.width // 2 - BULLET_SIZE // 2,
                        self.player.y
                    ))
                    
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move('left')
            if keys[pygame.K_RIGHT]:
                self.player.move('right')
                
        return True
    
    def update(self):
        if self.game_over:
            return
            
        # Move aliens
        move_down = False
        for alien in self.aliens:
            alien.move()
            if alien.x <= 0 or alien.x >= WIDTH - alien.width:
                move_down = True
                
        if move_down:
            for alien in self.aliens:
                alien.direction *= -1
                alien.y += 20
                alien.rect.y = alien.y
                if alien.y + alien.height >= self.player.y:
                    self.game_over = True
                    
        # Move bullets and check collisions
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
            else:
                for alien in self.aliens[:]:
                    if bullet.rect.colliderect(alien.rect):
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        self.aliens.remove(alien)
                        self.score += 10
                        
        # Check for win condition
        if not self.aliens:
            self.game_over = True
            
    def draw(self):
        screen.fill(BLACK)
        
        self.player.draw()
        for alien in self.aliens:
            alien.draw()
        for bullet in self.bullets:
            bullet.draw()
            
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            font = pygame.font.Font(None, 74)
            if self.aliens:
                text = font.render('Game Over!', True, RED)
            else:
                text = font.render('You Win!', True, GREEN)
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(text, text_rect)
            
        pygame.display.flip()

def main():
    game = Game()
    running = True
    
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
