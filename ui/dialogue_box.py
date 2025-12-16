import pygame

class DialogueBox:
    PADDING = 12

    def __init__(self, width=700, height=140, font=None):
        self.width = width
        self.height = height
        self.visible = False
        self.lines = []
        self.choices = None
        self.callback = None
        self.selected = 0
        self.font = font or pygame.font.Font(None, 28)
        self.rect = None

    def open(self, lines, choices=None, callback=None):
        self.lines = lines if isinstance(lines, list) else [str(lines)]
        self.choices = choices
        self.callback = callback
        self.selected = 0
        self.visible = True

    def close(self):
        self.visible = False
        self.lines = []
        self.choices = None
        self.callback = None

    def handle_event(self, event):
        if not self.visible: return
        if event.type == pygame.KEYDOWN:
            if self.choices:
                if event.key == pygame.K_UP: self.selected = (self.selected -1) % len(self.choices)
                if event.key == pygame.K_DOWN: self.selected = (self.selected +1) % len(self.choices)
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    if self.callback: self.callback(self.selected)
                    self.close()
            else:
                self.close()

    def draw(self, screen):
        if not self.visible: return
        sw, sh = screen.get_size()
        x = (sw - self.width)//2
        y = sh - self.height - 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, (30,30,30), self.rect)
        pygame.draw.rect(screen, (220,220,220), self.rect, 2)
        line_y = y + self.PADDING
        for line in self.lines:
            surf = self.font.render(line, True, (255,255,255))
            screen.blit(surf, (x + self.PADDING, line_y))
            line_y += surf.get_height() + 6
        if self.choices:
            choice_y = line_y + 6
            for i, choice in enumerate(self.choices):
                prefix = "→ " if i==self.selected else "  "
                color = (255,255,120) if i==self.selected else (200,200,200)
                surf = self.font.render(prefix+choice, True, color)
                screen.blit(surf, (x+self.PADDING, choice_y))
                choice_y += surf.get_height() + 4
