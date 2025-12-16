import pygame
from states.casino_floor import CasinoFloor
from states.bank import Bank
from states.game_over import GameOver
from states.roulette import Roulette
from states.blackjack import Blackjack
from states.slot_machine import SlotMachine

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casino")
clock = pygame.time.Clock()
FPS = 60

current_state = CasinoFloor()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if hasattr(current_state, "handle_event"):
            current_state.handle_event(event)

    if hasattr(current_state, "update"):
        current_state.update()

    # state switching logic
    next_state = getattr(current_state, "next_state", None)
    if next_state:
        player = getattr(current_state, "player", None)
        if next_state == "bank":
            current_state = Bank(player=player)
        elif next_state == "casino":
            current_state = CasinoFloor(player=player)
        elif next_state == "roulette":
            current_state = Roulette(player=player)
        elif next_state == "blackjack":
            current_state = Blackjack(player=player)
        elif next_state == "slot":
            current_state = SlotMachine(player=player)
        elif next_state == "game_over":
            current_state = GameOver()
        elif next_state == "restart":
            current_state = CasinoFloor()
        else:
            pass

    if hasattr(current_state, "draw"):
        current_state.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
