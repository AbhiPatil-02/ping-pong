import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.prev_x = x  # Track previous position for continuous collision detection

    def move(self):
        # Store previous position before moving
        self.prev_x = self.x
        self.prev_y = self.y
        
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        # Continuous collision detection for high speeds
        ball_rect = self.rect()
        
        # Check collision with player paddle
        if self.velocity_x < 0:  # Moving left toward player
            if self.continuous_collision_detection(player, ball_rect):
                self.handle_paddle_collision(player)
        
        # Check collision with AI paddle  
        elif self.velocity_x > 0:  # Moving right toward AI
            if self.continuous_collision_detection(ai, ball_rect):
                self.handle_paddle_collision(ai)

    def continuous_collision_detection(self, paddle, ball_rect):
        """Enhanced collision detection that checks the ball's path"""
        paddle_rect = paddle.rect()
        
        # Simple rectangle collision (works for normal speeds)
        if ball_rect.colliderect(paddle_rect):
            return True
        
        # Continuous collision detection for high speeds
        # Create a "swept" rectangle that represents the ball's movement path
        if self.velocity_x != 0 or self.velocity_y != 0:
            # Calculate the ball's movement vector
            move_rect = pygame.Rect(
                min(self.prev_x, self.x),
                min(self.prev_y, self.y),
                abs(self.velocity_x) + self.width,
                abs(self.velocity_y) + self.height
            )
            
            if move_rect.colliderect(paddle_rect):
                return True
        
        return False

    def handle_paddle_collision(self, paddle):
        """Handle collision with paddles including angle calculation"""
        paddle_rect = paddle.rect()
        ball_rect = self.rect()
        
        # Calculate where the ball hit the paddle (-1 to 1)
        relative_intersect_y = (paddle_rect.centery - ball_rect.centery) / (paddle_rect.height / 2)
        
        # Reverse X direction and adjust Y based on hit position
        self.velocity_x *= -1
        self.velocity_y = -relative_intersect_y * 5  # Adjust this multiplier for game feel
        
        # Ensure minimum speed
        min_speed = 3
        if abs(self.velocity_y) < min_speed:
            self.velocity_y = min_speed if self.velocity_y > 0 else -min_speed
        
        # Slight speed increase on each hit (optional)
        speed_increase = 1.05
        self.velocity_x *= speed_increase
        self.velocity_y *= speed_increase
        
        # Prevent the ball from getting stuck in the paddle
        if self.velocity_x > 0:  # Moving right
            self.x = paddle_rect.right + 1
        else:  # Moving left
            self.x = paddle_rect.left - self.width - 1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.prev_x = self.x
        self.prev_y = self.y

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)