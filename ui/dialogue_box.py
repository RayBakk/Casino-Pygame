import pygame

class DialogueBox:
    PADDING = 12
    LINE_SPACING = 6
    CHOICE_SPACING = 4
    MAX_CHOICE_HEIGHT = 300

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

        line_count = len(self.lines)
        choice_count = len(self.choices) if self.choices else 0
        needed_height = 2*self.PADDING + line_count*(self.font.get_height()+self.LINE_SPACING) \
                        + choice_count*(self.font.get_height()+self.CHOICE_SPACING)
        self.height = max(self.height, min(needed_height, self.MAX_CHOICE_HEIGHT))

    def close(self):
        self.visible = False
        self.lines = []
        self.choices = None
        self.callback = None

    def handle_event(self, event):
        if not self.visible: 
            return
        if event.type == pygame.KEYDOWN:
            if self.choices is not None:
                if event.key == pygame.K_UP: 
                    self.selected = (self.selected - 1) % len(self.choices)
                if event.key == pygame.K_DOWN: 
                    self.selected = (self.selected + 1) % len(self.choices)
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    if self.callback: 
                        self.callback(self.selected)
                    self.close()
            else:
                self.close()

    def draw(self, screen):
        if not self.visible: 
            return
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
            line_y += surf.get_height() + self.LINE_SPACING

        if self.choices:
            max_per_column = 10
            num_columns = (len(self.choices) + max_per_column - 1) // max_per_column
            for i, choice in enumerate(self.choices):
                col = i // max_per_column
                row = i % max_per_column
                choice_x = x + self.PADDING + col * (self.width // num_columns)
                choice_y = line_y + row * (self.font.get_height()+self.CHOICE_SPACING)
                prefix = "→ " if i == self.selected else "  "
                color = (255,255,120) if i == self.selected else (200,200,200)
                surf = self.font.render(prefix+choice, True, color)
                screen.blit(surf, (choice_x, choice_y))
