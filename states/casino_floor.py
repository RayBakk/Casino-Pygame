import pygame
from states.animated_door import AnimatedDoor

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ==================== Player ========================

class Player:
    def __init__(self, x=400, y=300):
        self.x = x
        self.y = y

        self.size = 40
        self.speed = 5

        self.sheet_path = "assets/player/player.png"
        self.load_sheet(self.sheet_path)
        self.frame_w = self.sheet.get_width() // 4
        self.frame_h = self.sheet.get_height() // 4

        self.dir_row = {
            "down": 0,
            "right": 1,
            "up": 2,
            "left": 3
        }

        self.direction = "down"
        self.moving = False

        self.frame = 0
        self.frame_timer = 0
        self.frame_delay = 120  # ms

        self.money = 1000
        self.loan_amount = 0
        self.loan_deadline_ms = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        self.moving = False

        if keys[pygame.K_z] or keys[pygame.K_UP]:
            dy = -self.speed
            self.direction = "up"
            self.moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
            self.direction = "down"
            self.moving = True
        elif keys[pygame.K_q] or keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "right"
            self.moving = True

        self.x += dx
        self.y += dy

    def update(self, width, height):
        self.handle_input()

        now = pygame.time.get_ticks()
        if self.moving:
            if now - self.frame_timer >= self.frame_delay:
                self.frame_timer = now
                self.frame = (self.frame + 1) % 4
        else:
            self.frame = 0

        self.apply_boundaries(width, height)

    def apply_boundaries(self, width, height):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.size > width:
            self.x = width - self.size
        if self.y + self.size > height:
            self.y = height - self.size

    def get_current_image(self):
        idle_col_for_row = {
            0: 1,  # down
            1: 1,  # right
            2: 1,  # up
            3: 0   # left
        }

        row = self.dir_row[self.direction]
        col = self.frame if self.moving else idle_col_for_row[row]

        rect = pygame.Rect(
            col * self.frame_w,
            row * self.frame_h,
            self.frame_w,
            self.frame_h
        )
        return self.sheet.subsurface(rect)

    def draw(self, screen):
        img = self.get_current_image()
        img = pygame.transform.scale(img, (self.size, self.size))
        screen.blit(img, (int(self.x), int(self.y)))

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    # LOANS
    def start_loan(self, amount: int, duration_seconds: int):
        if self.loan_active():
            return
        self.money += amount
        self.loan_amount = amount
        self.loan_deadline_ms = pygame.time.get_ticks() + duration_seconds * 1000

    def loan_active(self):
        return self.loan_deadline_ms is not None

    def loan_time_left_ms(self):
        if not self.loan_active():
            return 0
        return max(0, self.loan_deadline_ms - pygame.time.get_ticks())

    def loan_overdue(self):
        return self.loan_active() and pygame.time.get_ticks() > self.loan_deadline_ms

    def clear_loan(self):
        self.loan_amount = 0
        self.loan_deadline_ms = None
    
    def load_sheet(self, path: str):
        self.sheet_path = path
        self.sheet = pygame.image.load(path).convert_alpha()
        self.frame_w = self.sheet.get_width() // 4
        self.frame_h = self.sheet.get_height() // 4

    def set_skin(self, path: str):
        self.sheet = pygame.image.load(path).convert_alpha()
        self.frame_w = self.sheet.get_width() // 4
        self.frame_h = self.sheet.get_height() // 4



# ==================== CASINO FLOOR ========================

class CasinoFloor:
    def __init__(self, player: Player = None):
        self.player = player if player else Player()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.next_state = None

        self.floor_tile = pygame.image.load("assets/background/casino_floor_tile.png").convert_alpha()
        self.floor_tile = pygame.transform.scale(self.floor_tile, (64, 64))

        self.blackjack_img = pygame.image.load("assets/background/blackjack_casino_floor.png").convert_alpha()
        self.roulette_img = pygame.image.load("assets/background/roulette_casino_floor.png").convert_alpha()
        self.slot_img = pygame.image.load("assets/background/slots_casino_floor.png").convert_alpha()
        self.wardrobe_img = pygame.image.load("assets/background/wardrobe.png").convert_alpha()


        wardrobe_h =48
        self.wardrobe_rect = pygame.Rect(100, wardrobe_h, 48 , 48)

        self.blackjack_rect = pygame.Rect(90, 120, 140, 90)
        self.roulette_rect = pygame.Rect(270, 100, 170, 120)
        self.slot_rect = pygame.Rect(520, 120, 70, 120)

        self.door = AnimatedDoor(
            sheet_path="assets/background/EntranceDoorAnimationSheet.png",
            pos=((SCREEN_WIDTH - (pygame.image.load("assets/background/EntranceDoorAnimationSheet.png").get_width() // 9)) // 2,0 ),            frames_count=9,
            delay=50
        )

        self.interact_padding = 20

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            p = self.player.rect()
            if p.colliderect(self.roulette_rect.inflate(self.interact_padding, self.interact_padding)):
                self.next_state = "roulette"
            elif p.colliderect(self.blackjack_rect.inflate(self.interact_padding, self.interact_padding)):
                self.next_state = "blackjack"
            elif p.colliderect(self.slot_rect.inflate(self.interact_padding, self.interact_padding)):
                self.next_state = "slot"
            elif p.colliderect(self.door.rect.inflate(self.interact_padding, self.interact_padding)):
                self.next_state = "bank"
            elif p.colliderect(self.wardrobe_rect.inflate(self.interact_padding, self.interact_padding)):
                self.next_state = "wardrobe"


    def update(self):
        self.player.update(self.width, self.height)

        near_door = self.player.rect().colliderect(self.door.rect.inflate(60, 60))
        self.door.update(near_door)

        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw_tiled_floor(self, screen):
        tw, th = self.floor_tile.get_size()
        for y in range(0, self.height, th):
            for x in range(0, self.width, tw):
                screen.blit(self.floor_tile, (x, y))

    def draw(self, screen):
        self.draw_tiled_floor(screen)

        bj = pygame.transform.scale(self.blackjack_img, (self.blackjack_rect.w, self.blackjack_rect.h))
        ro = pygame.transform.scale(self.roulette_img, (self.roulette_rect.w, self.roulette_rect.h))
        sl = pygame.transform.scale(self.slot_img, (self.slot_rect.w, self.slot_rect.h))

        screen.blit(bj, self.blackjack_rect.topleft)
        screen.blit(ro, self.roulette_rect.topleft)
        screen.blit(sl, self.slot_rect.topleft)

        self.door.draw(screen)

        wardrobe_draw = pygame.transform.scale(self.wardrobe_img, (self.wardrobe_rect.w, self.wardrobe_rect.h))
        screen.blit(wardrobe_draw, self.wardrobe_rect.topleft)

        self.player.draw(screen)

        hud_font = pygame.font.Font(None, 28)
        screen.blit(hud_font.render(f"Money: ${self.player.money}", True, (255, 255, 255)), (10, 10))

        if self.player.loan_active():
            sec_left = self.player.loan_time_left_ms() // 1000
            screen.blit(
                hud_font.render(f"Loan: ${self.player.loan_amount} - Time left: {sec_left}s", True, (255, 200, 50)),
                (10, 30)
            )

        help_font = pygame.font.Font(None, 20)
        screen.blit(help_font.render("Press E when near a table/machine/door.", True, (220, 220, 220)),
                    (10, self.height - 30))
