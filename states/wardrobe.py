import pygame
from states.casino_floor import SCREEN_WIDTH, SCREEN_HEIGHT, Player

class Wardrobe:
    def __init__(self, player: Player = None):
        # initialiseren van variables
        self.player = player
        self.next_state = None

        # gets every asset from skin
        self.skins = [f"assets/player/skins/{i}.png" for i in range(1, 17)]
        self.selected = 0

        # initialzing font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 22)

        # some variables for the grid
        self.cols = 5
        self.cell_size = 96
        self.start_x = 80
        self.start_y = 140


        # load the preview for the skins
        self.thumbs = []
        for path in self.skins:
            img = pygame.image.load(path).convert_alpha()
            self.thumbs.append(pygame.transform.scale(img, (64, 64)))

        # event handler for possible events
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                self.next_state = "casino"
                return

            if event.key in (pygame.K_e, pygame.K_RETURN):
                self.player.load_sheet(self.skins[self.selected])
                self.next_state = "casino"
                return

            if event.key == pygame.K_RIGHT:
                if self.selected + 1 < len(self.skins):
                    self.selected += 1

            elif event.key == pygame.K_LEFT:
                if self.selected - 1 >= 0:
                    self.selected -= 1

            elif event.key == pygame.K_DOWN:
                nxt = self.selected + self.cols
                if nxt < len(self.skins):
                    self.selected = nxt

            elif event.key == pygame.K_UP:
                nxt = self.selected - self.cols
                if nxt >= 0:
                    self.selected = nxt
    # veiligheidscheck
    def update(self):
        if self.player.loan_overdue():
            self.next_state = "game_over"

    # draw
    def draw(self, screen):
        screen.fill((25, 25, 30))

        title = self.font.render("Wardrobe - Choose your character", True, (240, 240, 240))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        hint = self.small_font.render("Arrows = select | E / Enter = equip | ESC = back", True, (200, 200, 200))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 80))

        # grid tekenen
        for i, img in enumerate(self.thumbs):
            row = i // self.cols
            col = i % self.cols

            x = self.start_x + col * self.cell_size
            y = self.start_y + row * self.cell_size

            # highlight
            if i == self.selected:
                pygame.draw.rect(screen,(255, 215, 0), (x - 6, y - 6, 76, 76), 3)
            screen.blit(img, (x, y))

        footer = self.small_font.render(f"Selected skin: {self.selected + 1}.png", True, (220, 220, 220))
        screen.blit(footer, (10, SCREEN_HEIGHT - 30))