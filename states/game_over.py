import pygame

class GameOver:
    def __init__(self):
        self.next_state = None
        self.font_big = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.next_state = "restart"
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((10, 10, 10))

        title = self.font_big.render("GAME OVER", True, (200, 30, 30))
        reason = self.font_small.render("You failed to repay your loan and ended up in the street.", True, (220, 220, 220))
        restart = self.font_small.render("Press R to restart or ESC to quit", True, (200, 200, 200))

        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 200))
        screen.blit(reason, (screen.get_width()//2 - reason.get_width()//2, 300))
        screen.blit(restart, (screen.get_width()//2 - restart.get_width()//2, 350))
