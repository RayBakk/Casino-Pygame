import pygame
import random
from states.casino_floor import Player, SCREEN_WIDTH, SCREEN_HEIGHT

class SlotMachine:
    def __init__(self, player: Player):
        self.player = player
        self.next_state = None

        self.symbols = ["CHERRY", "LEMON", "BELL", "DIAMOND"]
        self.reels = ["?", "?", "?"]

        self.spin_cost = 50
        self.message = "Press SPACE to spin ($50). ESC to exit."
        self.spinning = False
        self.spin_end_time = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "casino"
            elif event.key == pygame.K_SPACE and not self.spinning:
                self.start_spin()

    def start_spin(self):
        if self.player.money < self.spin_cost:
            self.message = "Not enough money!"
            return

        self.player.money -= self.spin_cost
        self.spinning = True
        self.spin_end_time = pygame.time.get_ticks() + 800
        self.message = "Spinning..."

    def finish_spin(self):
        self.reels = [random.choice(self.symbols) for _ in range(3)]
        self.spinning = False
        self.check_win()

    def check_win(self):
        if self.reels.count(self.reels[0]) == 3:
            symbol = self.reels[0]
            payout = {
                "CHERRY": 100,
                "LEMON": 150,
                "BELL": 300,
                "DIAMOND": 1000
            }[symbol]

            self.player.money += payout
            self.message = f"3x {symbol}! You won ${payout}!"
        else:
            self.message = "No match. You lost."

    def update(self):
        if self.spinning and pygame.time.get_ticks() >= self.spin_end_time:
            self.finish_spin()

        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw(self, screen):
        screen.fill((20, 20, 20))
        font_big = pygame.font.Font(None, 64)
        font = pygame.font.Font(None, 28)

        title = font_big.render("SLOT MACHINE", True, (255, 255, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))

        # reels
        for i, symbol in enumerate(self.reels):
            x = 260 + i * 100
            y = 250
            pygame.draw.rect(screen, (80,80,80), (x, y, 80, 80))
            text = font.render(symbol, True, (255,255,255))
            screen.blit(text, (x + 40 - text.get_width()//2, y + 40 - text.get_height()//2))

        # HUD
        screen.blit(font.render(f"Money: ${self.player.money}", True, (255,255,255)), (20, 20))
        screen.blit(font.render(self.message, True, (200,200,200)), (200, 360))

        if self.player.loan_active():
            sec = self.player.loan_time_left_ms() // 1000
            screen.blit(
                font.render(f"Loan: ${self.player.loan_amount} - {sec}s left", True, (255,200,50)),
                (20, 50)
            )
