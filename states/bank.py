import pygame
from ui.dialogue_box import DialogueBox
from states.casino_floor import Player, SCREEN_WIDTH, SCREEN_HEIGHT
from states.animated_door import AnimatedDoor

class Bank:
    def __init__(self, player: Player = None):
        # initialiseren van variables
        self.player = player
        self.player.x = 380
        self.player.y = 520

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.next_state = None
        self.dialogue = DialogueBox()

        # NPC rect
        self.npc_rect = pygame.Rect(360, 200, 80, 100)

        # assets
        self.tile = pygame.image.load("assets/background/bank_tile.png").convert_alpha()
        self.tile = pygame.transform.scale(self.tile, (64, 64))

        self.teller_img = pygame.image.load("assets/background/bank_teller.png").convert_alpha()
        self.teller_draw_size = (self.npc_rect.w, self.npc_rect.h)

        # deur (animated)
        self.door = AnimatedDoor(sheet_path="assets/background/EntranceDoorAnimationSheet.png",
            pos=((SCREEN_WIDTH - (pygame.image.load("assets/background/EntranceDoorAnimationSheet.png").get_width() // 9)) // 2,
            SCREEN_HEIGHT - pygame.image.load("assets/background/EntranceDoorAnimationSheet.png").get_height()),
            frames_count=9,delay=50)

        self.interact_padding = 20

    def handle_event(self, event):
        if self.dialogue.visible:
            self.dialogue.handle_event(event)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.player.rect().colliderect(self.npc_rect.inflate(self.interact_padding, self.interact_padding)):
                self.open_npc_menu()
            elif self.player.rect().colliderect(self.door.rect.inflate(self.interact_padding, self.interact_padding)):
                self.player.x = 380
                self.player.y = 40
                self.next_state = "casino"

    def open_npc_menu(self):
        lines = ["Bank Teller: Welcome! What would you like to do?"]
        choices = []
        if self.player.loan_active() == False:
            choices.append("Take loan $500 (60s to repay)")
            choices.append("Take loan $1000 (120s to repay)")
        else:
            choices.append("Repay loan")
        choices.append("Leave")

        def callback(choice):
            if self.player.loan_active() == False:
                if choice == 0:
                    self.player.start_loan(500, 60)
                elif choice == 1:
                    self.player.start_loan(1000, 120)
            else:
                if choice == 0:
                    if self.player.money >= self.player.loan_amount:
                        self.player.money -= self.player.loan_amount
                        self.player.clear_loan()
                    else:
                        self.dialogue.open(["Bank Teller: You don't have enough money to repay!"])

        self.dialogue.open(lines, choices, callback)

    def update(self):
        if not self.dialogue.visible:
            self.player.update(self.width, self.height)

        # deur open/dicht animatie
        near_door = self.player.rect().colliderect(self.door.rect.inflate(60, 60))
        self.door.update(near_door)

        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw_tiled_bg(self, screen):
        tw, th = self.tile.get_size()
        for y in range(0, self.height, th):
            for x in range(0, self.width, tw):
                screen.blit(self.tile, (x, y))

    def draw(self, screen):
        # background tiles
        self.draw_tiled_bg(screen)

        # teller sprite
        teller = pygame.transform.scale(self.teller_img, self.teller_draw_size)
        screen.blit(teller, self.npc_rect.topleft)

        # deur (animated)
        self.door.draw(screen)

        # player
        self.player.draw(screen)

        # labels + HUD
        font = pygame.font.Font(None, 26)
        screen.blit(font.render("Bank Teller", True, (20, 20, 20)), (self.npc_rect.x, self.npc_rect.y - 22))

        hud_font = pygame.font.Font(None, 28)
        screen.blit(hud_font.render(f"Money: ${self.player.money}", True, (20, 20, 20)), (10, 10))

        if self.player.loan_active():
            sec_left = self.player.loan_time_left_ms() // 1000
            screen.blit(hud_font.render(f"Loan: ${self.player.loan_amount} - Time left: {sec_left}s", True, (120, 60, 0)), (10, 30))

        help_font = pygame.font.Font(None, 20)
        screen.blit(help_font.render("Press E to talk to the teller when near him.", True, (30, 30, 30)),
                    (10, self.height - 30))
        
        self.dialogue.draw(screen)