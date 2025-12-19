import pygame

class DialogueBox:
    padding = 12
    line_spacing = 6
    choice_spacing = 4
    max_choice_length = 300

    def __init__(self, width=700, height=140, font=None):
        self.width = width
        self.base_height = height
        self.height = height
        self.visible = False
        self.lines = []
        self.choices = None
        self.callback = None
        self.selected = 0
        if font is not None:
            self.font = font
        else:
            self.font = pygame.font.Font(None, 28)
        self.rect = None

    def open(self, lines, choices=None, callback=None):
        if isinstance(lines, list):
            self.lines = lines
        else:
            self.lines = [str(lines)]
        self.choices = choices
        self.callback = callback
        self.selected = 0
        self.visible = True

        line_count = len(self.lines)
        if self.choices is not None:
            choice_count = len(self.choices)
        else: 
            choice_count = 0
        needed_height = 2*self.padding + line_count*(self.font.get_height()+self.line_spacing) + choice_count*(self.font.get_height()+self.choice_spacing)
        self.height = min(max(self.base_height, needed_height), self.max_choice_length)

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

    def draw(self, screen, ):
        if not self.visible: 
            return
        sw, sh = screen.get_size()
        x = (sw - self.width)//2
        y = sh - self.height - 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, (30,30,30), self.rect)
        pygame.draw.rect(screen, (220,220,220), self.rect, 2)

        line_y = y + self.padding

        for line in self.lines:
            surf = self.font.render(line, True, (255,255,255))
            screen.blit(surf, (x + self.padding, line_y))
            line_y += surf.get_height() + self.line_spacing

        if self.choices:
            max_per_column = 10
            num_columns = (len(self.choices) + max_per_column - 1) // max_per_column
            for i, choice in enumerate(self.choices):
                col = i // max_per_column
                row = i % max_per_column
                choice_x = x + self.padding + col * (self.width // num_columns)
                choice_y = line_y + row * (self.font.get_height()+self.choice_spacing)
                if i == self.selected:
                    prefix = "X "
                    color = (255, 255, 120)
                else:
                    prefix = " "
                    color = (200, 200, 200)
                surf = self.font.render(prefix+choice, True, color)
                screen.blit(surf, (choice_x, choice_y))
