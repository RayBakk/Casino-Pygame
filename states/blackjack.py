import pygame
import random
from states.casino_floor import Player, SCREEN_WIDTH, SCREEN_HEIGHT
from ui.dialogue_box import DialogueBox

class Blackjack:
    def __init__(self, player: Player = None):
        self.player = player
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.next_state = None
        self.dialogue = DialogueBox()

        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]*4
        self.player_hand = []
        self.dealer_hand = []

        self.bet_amount = 100
        self.round_active = False

        self.message = "Press SPACE to start a new round, ESC to exit."

    def handle_event(self, event):
        if self.dialogue.visible:
            self.dialogue.handle_event(event)
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "casino"
            elif event.key == pygame.K_SPACE and self.round_active == False:
                self.start_round()
            elif event.key == pygame.K_h and self.round_active == True:
                self.player_hit()
            elif event.key == pygame.K_s and self.round_active == True:
                self.player_stand()
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
    def show_help(self):
        lines = [
            "Goal: Get as close to 21 as possible without going over.",
            "Controls: - UP : Increase bet - DOWN : Decrease bet",
            "Card values: - Number cards are worth their number", 
            "- Face cards (J, Q, K) are worth 10", 
            "- Aces are worth 11 or 1",
            "Rules:",
            "- Dealer draws until at least 17",
            "- Going over 21 is a BUST and you lose",
            "- If you beat the dealer, you win",
            "- Same value as dealer is a tie",
        ]

        choices = ["Close"]
        self.dialogue.open(lines, choices)

    def start_round(self):
        if self.player.money < self.bet_amount:
            self.message = "Not enough money to bet!"
            return

        self.round_active = True
        self.player.money -= self.bet_amount
        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,11]*4
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.message = "Press H to Hit, S to Stand"

        if self.hand_value(self.player_hand) == 21:
            self.end_round(won=True)


    def player_hit(self):
        if self.round_active == False:
            return

        self.player_hand.append(self.deck.pop())

        if self.hand_value(self.player_hand) > 21:
            self.end_round(lost=True)

    def player_stand(self):
        if not self.round_active:
            return
        
        # dealer plays
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        # compare hands
        player_val = self.hand_value(self.player_hand)
        dealer_val = self.hand_value(self.dealer_hand)
        if dealer_val > 21 or player_val > dealer_val:
            self.end_round(won=True)
        elif player_val == dealer_val:
            self.end_round(tie=True)
        else:
            self.end_round(lost=True)

    def hand_value(self, hand):
        value = sum(hand)

        # adjust for Aces
        aces = hand.count(11)
        while value > 21 and aces == True:
            value -= 10
            aces -= 1
        return value

    def end_round(self, won=False, lost=False, tie=False):
        self.round_active = False
        if won:
            self.player.money += self.bet_amount*2
            self.message = f"You won! You got ${self.bet_amount*2}."
        elif tie:
            self.player.money += self.bet_amount
            self.message = "It's a tie! Your bet is returned."
        else:
            self.message = "You lost the bet."

    def update(self):
        # loan overdue
        if self.player.loan_overdue():
            self.next_state = "game_over"

    def draw(self, screen):
        # green table background
        screen.fill((43, 146, 115))  
        font = pygame.font.Font(None, 28)
        screen.blit(font.render("Blackjack - H: Hit, S: Stand, SPACE: New Round, ESC: Exit", True, (255,255,255)), (120, 60))
        pygame.draw.rect(screen, (255,255,255), (50, 150, 700, 200), 2)

        # player hand
        player_val = self.hand_value(self.player_hand)
        player_text = f"Player: {', '.join(map(str, self.player_hand))} ({player_val})"
        screen.blit(font.render(player_text, True, (255,255,255)), (60, 160))

        # dealer hand
        dealer_val = self.hand_value(self.dealer_hand)
        dealer_text = f"Dealer: {', '.join(map(str, self.dealer_hand))} ({dealer_val})"
        screen.blit(font.render(dealer_text, True, (255,255,255)), (60, 220))
    
        # HUD
        screen.blit(font.render(f"Bet: ${self.bet_amount}", True, (255,255,255)), (10, 90))
        screen.blit(font.render(f"Money: ${self.player.money}", True, (255,255,255)), (10, 10))
        if self.player.loan_active():
            sec_left = self.player.loan_time_left_ms()//1000
            screen.blit(font.render(f"Loan: ${self.player.loan_amount} - Time left: {sec_left}s", True, (255,200,50)), (10, 30))

        # start message
        screen.blit(font.render(self.message, True, (255,255,0)), (50, 400))
        
        # help message
        self.dialogue.draw(screen)