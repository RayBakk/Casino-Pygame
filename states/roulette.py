import pygame
import random
from states.casino_floor import Player, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.dialogue_box import DialogueBox

class Roulette:
    def __init__(self, player: Player):
        self.player = player
        self.next_state = None
        self.dialogue = DialogueBox()
        self.pending_message = None

        # European roulette wheel
        self.wheel = [
            0, 32, 15, 19, 4, 21, 2, 25, 17,
            34, 6, 27, 13, 36, 11, 30, 8,
            23, 10, 5, 24, 16, 33, 1, 20,
            14, 31, 9, 22, 18, 29, 7, 28,
            12, 35, 3, 26
        ]

        self.red_numbers = {
            1,3,5,7,9,12,14,16,18,
            19,21,23,25,27,30,32,34,36
        }

        self.bet_amount = 100
        self.message = "Press E to place a bet, ESC to exit."

    def handle_event(self, event):
        if self.dialogue.visible:
            self.dialogue.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "casino"
            elif event.key == pygame.K_e:
                self.open_bet_menu()
        
        if event.type == pygame.USEREVENT and self.pending_message:
            self.dialogue.open(self.pending_message)
            self.pending_message = None
            pygame.time.set_timer(pygame.USEREVENT, 0)


    def open_bet_menu(self):
        lines = ["Roulette - Choose your bet ($100):"]
        choices = [
            "Red (x2)",
            "Black (x2)",
            "Even (x2)",
            "Odd (x2)",
            "Single Number (x36)",
            "Cancel"
        ]

        def callback(choice):
            if choice == 0:
                self.spin("red")
            elif choice == 1:
                self.spin("black")
            elif choice == 2:
                self.spin("even")
            elif choice == 3:
                self.spin("odd")
            elif choice == 4:
                self.choose_number()
        self.dialogue.open(lines, choices, callback)

    def choose_number(self):
        lines = ["Choose a number between 0 and 36:"]
        choices = [str(i) for i in range(0, 37)]

        def callback(idx):
            self.spin("number", int(choices[idx]))

        self.dialogue.open(lines, choices, callback)

    def spin(self, bet_type, bet_value=None):
        if self.player.money < self.bet_amount:
            self.dialogue.open(["You don't have enough money!"])
            return

        self.player.money -= self.bet_amount
        result = random.choice(self.wheel)

        win = False
        payout = 0

        if bet_type == "red":
            win = result in self.red_numbers
            payout = 2
        elif bet_type == "black":
            win = result != 0 and result not in self.red_numbers
            payout = 2
        elif bet_type == "even":
            win = result != 0 and result % 2 == 0
            payout = 2
        elif bet_type == "odd":
            win = result % 2 == 1
            payout = 2
        elif bet_type == "number":
            win = result == bet_value
            payout = 36

        if win:
            winnings = self.bet_amount * payout
            self.player.money += winnings
            result_text = [
                f"Ball landed on {result}.",
                f"You WON ${winnings}!"
            ]
        else:
            result_text = [
                f"Ball landed on {result}.",
                "You lost your bet."
            ]

        # IMPORTANT: open dialogue AFTER menu closes
        pygame.time.set_timer(pygame.USEREVENT, 100)
        self.pending_message = result_text


    def update(self):
        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw(self, screen):
        screen.fill((30, 100, 30))

        font = pygame.font.Font(None, 32)
        big = pygame.font.Font(None, 40)

        title = big.render("Roulette Table", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))

        screen.blit(font.render(self.message, True, (230,230,230)), (200, 90))
        screen.blit(font.render(f"Money: ${self.player.money}", True, (255,255,255)), (20, 20))

        if self.player.loan_active():
            sec = self.player.loan_time_left_ms() // 1000
            screen.blit(
                font.render(f"Loan: ${self.player.loan_amount} - {sec}s left", True, (255,200,50)),
                (20, 50)
            )

        pygame.draw.circle(screen, (0,0,0), (400, 320), 140)
        pygame.draw.circle(screen, (200,0,0), (400, 320), 130)

        self.dialogue.draw(screen)
