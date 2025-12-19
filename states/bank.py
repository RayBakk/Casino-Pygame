import pygame
from ui.dialogue_box import DialogueBox
from states.casino_floor import Player, SCREEN_WIDTH, SCREEN_HEIGHT

class Bank:
    def __init__(self, player: Player = None):
        self.player = player
        self.player.x = 380
        self.player.y = 520
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.door_rect = pygame.Rect(350, 580, 100, 20)
        self.next_state = None
        self.npc_rect = pygame.Rect(360, 200, 80, 100)
        self.dialogue = DialogueBox()

         # ================= ASSETS =================
        self.floor_tile = pygame.image.load("assets/background/casino_floor_tile.png").convert_alpha()
        self.floor_tile = pygame.transform.scale(self.floor_tile, (64, 64))

    def handle_event(self, event):
        if self.dialogue.visible:
            self.dialogue.handle_event(event)
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.player.rect().colliderect(self.npc_rect):
                self.open_npc_menu()
            elif self.player.rect().colliderect(self.door_rect):
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
                if choice == 0: self.player.start_loan(500, 60)
                elif choice == 1: self.player.start_loan(1000, 120)
            else:
                if choice == 0:
                    if self.player.money >= self.player.loan_amount:
                        self.player.money -= self.player.loan_amount
                        self.player.clear_loan()
                    else:
                        self.dialogue.open(["Bank Teller: You don't have enough money to repay!"])
        self.dialogue.open(lines, choices, callback)

    def update(self):
        if self.dialogue.visible == False:
            self.player.update(self.width, self.height)

        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw(self, screen):
        screen.fill((80, 80, 200))
        pygame.draw.rect(screen, (200,160,120), self.npc_rect)

        font = pygame.font.Font(None,26)
        screen.blit(font.render("Bank Teller", True, (255,255,255)), (self.npc_rect.x, self.npc_rect.y-22))
        
        self.player.draw(screen)
        pygame.draw.rect(screen, (200,200,0), self.door_rect)
        
        hud_font = pygame.font.Font(None,28)
        screen.blit(hud_font.render(f"Money: ${self.player.money}", True, (255,255,255)), (10,10))

        if self.player.loan_active():
            sec_left = self.player.loan_time_left_ms()//1000
            screen.blit(hud_font.render(f"Loan: ${self.player.loan_amount} - Time left: {sec_left}s", True, (255,200,50)), (10,30))
        
        help_font = pygame.font.Font(None,20)
        screen.blit(help_font.render("Press E to talk to the teller when near him.", True, (220,220,220)), (10,self.height-30))
        
        self.dialogue.draw(screen)
