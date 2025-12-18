import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player:
    def __init__(self, x=400, y=300):
        self.x = x
        self.y = y
        self.size = 40
        self.speed = 5
        self.money = 1000
        self.loan_amount = 0
        self.loan_deadline_ms = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        self.x += dx
        self.y += dy

    def apply_boundaries(self, width, height):
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        if self.x + self.size > width: self.x = width - self.size
        if self.y + self.size > height: self.y = height - self.size

    def update(self, width, height):
        self.handle_input()
        self.apply_boundaries(width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect())

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def start_loan(self, amount: int, duration_seconds: int):
        if self.loan_active():
            return
        self.money += amount
        self.loan_amount = amount
        self.loan_deadline_ms = pygame.time.get_ticks() + duration_seconds * 1000

    def loan_active(self):
        return self.loan_deadline_ms is not None

    def loan_time_left_ms(self):
        if self.loan_active() == False: 
            return 0
        return max(0, self.loan_deadline_ms - pygame.time.get_ticks())

    def loan_overdue(self):
        return self.loan_active() and (pygame.time.get_ticks() > self.loan_deadline_ms)

    def clear_loan(self):
        self.loan_amount = 0
        self.loan_deadline_ms = None

class CasinoFloor:
    def __init__(self, player: Player = None):
        self.player = player if player else Player()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.next_state = None
        # bank door
        self.door_rect = pygame.Rect(350, 0, 100, 20)
        # roulette
        self.roulette_rect = pygame.Rect(250, 120, 80, 60)
        # blackjack
        self.blackjack_rect = pygame.Rect(100, 120, 80, 60)
        # slot machine
        self.slot_rect = pygame.Rect(400, 120, 80, 60)


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.player.rect().colliderect(self.roulette_rect):
                self.next_state = "roulette"
            elif self.player.rect().colliderect(self.blackjack_rect):
                self.next_state = "blackjack"
            elif self.player.rect().colliderect(self.slot_rect):
                self.next_state = "slot"
            elif self.player.rect().colliderect(self.door_rect):
                self.next_state = "bank"

    def update(self):
        self.player.update(self.width, self.height)
        # loan check
        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw(self, screen):
        screen.fill((20, 120, 20))
        font = pygame.font.Font(None,26)
        # player
        self.player.draw(screen)
        # door
        pygame.draw.rect(screen, (200, 200, 0), self.door_rect)
        # roulette
        screen.blit(font.render("Roulette", True, (255,255,255)), (self.roulette_rect.x+3, self.roulette_rect.y-22))
        pygame.draw.rect(screen, (255, 0, 0), self.roulette_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.roulette_rect.inflate(-10, -10))
        # blackjack
        screen.blit(font.render("Blackjack", True, (255,255,255)), (self.blackjack_rect.x+3, self.blackjack_rect.y-22))
        pygame.draw.rect(screen, (0, 0, 0), self.blackjack_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.blackjack_rect.inflate(-10, -10))
        # slot machine
        screen.blit(font.render("Slot Machine", True, (255,255,255)), (self.slot_rect.x, self.slot_rect.y-22))
        pygame.draw.rect(screen, (120, 0, 120), self.slot_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.slot_rect.inflate(-10, -10))
        # HUD
        font = pygame.font.Font(None, 28)
        screen.blit(font.render(f"Money: ${self.player.money}", True, (255,255,255)), (10, 10))
        if self.player.loan_active():
            sec_left = self.player.loan_time_left_ms()//1000
            screen.blit(font.render(f"Loan: ${self.player.loan_amount} - Time left: {sec_left}s", True, (255,200,50)), (10, 30))
        help_font = pygame.font.Font(None,20)
        screen.blit(help_font.render("Press E to start a game when near to a machine.", True, (220,220,220)), (10,self.height-30))
