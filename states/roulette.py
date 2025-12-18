import pygame
import random
from states.casino_floor import Player, SCREEN_WIDTH
from ui.dialogue_box import DialogueBox

class Roulette:
    def __init__(self, player: Player = None):
        self.player = player if player else Player()
        self.next_state = None
        self.dialogue = DialogueBox()
        self.queued_action = None  # new: queue next dialogue action

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

        if self.queued_action:
            # Execute queued action when previous dialogue is closed (borrowed from chatgpt because didnt found the fix)
            self.queued_action()
            self.queued_action = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "casino"
            elif event.key == pygame.K_e:
                self.open_bet_menu()
            elif event.key == pygame.K_UP:
                self.bet_amount += 50
            elif event.key == pygame.K_DOWN and self.bet_amount > 50:
                self.bet_amount -= 50
            elif event.key == pygame.K_i:
                self.show_help()

    def show_help(self):
        lines = ["Help message..."]
        choices = ["Close"]

        self.dialogue.open(lines, choices)



    def open_bet_menu(self):
        lines = [f"Roulette - Choose your bet (${self.bet_amount}):"]
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
                # Queue the number selection to run after this dialogue closes
                self.queued_action = self.choose_number
            elif choice == 5:
                pass  # Cancel

        self.dialogue.open(lines, choices, callback)

    def choose_number(self):
        lines = ["Choose a number between 0 and 36:"]
        choices = [str(i) for i in range(0, 37)]

        def callback(choice):
            number = int(choices[choice])
            self.spin("number", number)

        self.dialogue.open(lines, choices, callback)

    def spin(self, bet_type, bet_value=None):
        if self.player.money < self.bet_amount:
            # Queue the "not enough money" message
            self.queued_action = lambda: self.dialogue.open(["You don't have enough money!"])
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
            result_text = [f"Ball landed on {result}.", f"You WON ${winnings}!"]
        else:
            result_text = [f"Ball landed on {result}.", "You lost your bet."]

        # Queue the spin result to display after any current dialogue closes
        self.queued_action = lambda: self.dialogue.open(result_text)


    def update(self):
        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw(self, screen):
        screen.fill((0, 120, 0))
        font = pygame.font.Font(None, 28)
        title_font = pygame.font.Font(None, 40)

        title = title_font.render("Roulette Table", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        screen.blit(font.render(self.message, True, (230, 230, 230)), (200, 90))
        screen.blit(font.render(f"Bet: ${self.bet_amount}", True, (255,255,255)), (10, 90))
        screen.blit(font.render(f"Money: ${self.player.money}", True, (255, 255, 255)), (10, 10))
        if self.player.loan_active():
            sec_left = self.player.loan_time_left_ms() // 1000
            screen.blit(font.render(f"Loan: ${self.player.loan_amount} - Time left: {sec_left}s", True, (255, 200, 50)), (10, 30))

        pygame.draw.circle(screen, (0, 0, 0), (400, 320), 140)
        pygame.draw.circle(screen, (200, 0, 0), (400, 320), 130)

        self.dialogue.draw(screen)
