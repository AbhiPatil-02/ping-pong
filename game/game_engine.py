import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5
        self.game_over = False
        self.winner = None
        
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 50)

    def handle_input(self):
        if self.game_over:
            # Check for restart or exit keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.restart_game()
            elif keys[pygame.K_q]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return
            
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.check_game_over()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.check_game_over()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self):
        """Check if either player has reached the winning score"""
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player"
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner = "AI"

    def restart_game(self):
        """Reset the game to initial state"""
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()
        
        # Reset paddle positions
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # Draw game over screen if game is over
        if self.game_over:
            self.render_game_over(screen)

    def render_game_over(self, screen):
        """Display the game over screen with winner information"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))

        # Winner message
        winner_text = self.large_font.render(f"{self.winner} Wins!", True, WHITE)
        screen.blit(winner_text, (self.width//2 - winner_text.get_width()//2, self.height//2 - 50))

        # Instructions
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(restart_text, (self.width//2 - restart_text.get_width()//2, self.height//2 + 20))

        # Final score
        score_text = self.font.render(f"Final Score: {self.player_score} - {self.ai_score}", True, WHITE)
        screen.blit(score_text, (self.width//2 - score_text.get_width()//2, self.height//2 + 70))