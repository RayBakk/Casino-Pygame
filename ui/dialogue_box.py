import pygame

class DialogueBox:
    padding = 12          # space between text and box edges
    line_spacing = 6      # space between lines of text
    choice_spacing = 4    # space between choices
    max_length = 300      # maximum height of the dialogue box

    def __init__(self, width=700, height=140, font=None):
        self.width = width
        self.base_height = height
        self.height = height
        # is the dialogue currently displayed
        self.visible = False       
        # list of text lines to display
        self.lines = []            
        # optional list of choices for player selection
        self.choices = None        
        # function to call when a choice is selected
        self.callback = None       
        # index of currently selected choice        
        self.selected = 0          
        # use given font, otherwise default pygame font
        if font is not None:
            self.font = font
        else:
            self.font = pygame.font.Font(None, 28)
        # rect object representing dialogue box area
        self.rect = None           

    def open(self, lines, choices=None, callback=None):
        # ensure lines is a list
        if isinstance(lines, list):
            self.lines = lines
        else:
            self.lines = [str(lines)]
        
        self.choices = choices
        self.callback = callback
        self.selected = 0
        self.visible = True

        # calculate required height for lines + choices
        line_count = len(self.lines)
        choice_count = len(self.choices) if self.choices is not None else 0
        needed_height = (2*self.padding + line_count*(self.font.get_height() + self.line_spacing) + choice_count*(self.font.get_height() + self.choice_spacing))
        # limit height between base height and max length
        self.height = min(max(self.base_height, needed_height), self.max_length)

    def close(self):
        self.visible = False
        self.lines = []
        self.choices = None
        self.callback = None

    def handle_event(self, event):
        if not self.visible: 
            return

        if event.type == pygame.KEYDOWN:
            # navigation only if there are choices
            if self.choices is not None:
                if event.key == pygame.K_UP: 
                    # move selection up and wrap around
                    self.selected = (self.selected - 1) % len(self.choices)
                if event.key == pygame.K_DOWN: 
                    # move selection down and wrap around
                    self.selected = (self.selected + 1) % len(self.choices)
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    # confirm selection
                    if self.callback: 
                        self.callback(self.selected)
                    self.close()
            else:
                # no choices
                self.close()

    def draw(self, screen):
        if not self.visible: 
            return

        # center horizontally
        sw, sh = screen.get_size()
        x = (sw - self.width) // 2
        y = sh - self.height - 20
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # draw background rectangle
        pygame.draw.rect(screen, (30,30,30), self.rect)
        # draw border
        pygame.draw.rect(screen, (220,220,220), self.rect, 2)
        # y position for first line
        line_y = y + self.padding 

        # draw text lines
        for line in self.lines:
            surf = self.font.render(line, True, (255,255,255))
            screen.blit(surf, (x + self.padding, line_y))
            line_y += surf.get_height() + self.line_spacing

        # draw choices if any
        if self.choices:
            # max number of choices per column
            max_per_column = 10  
            # calculate number of columns needed
            num_columns = (len(self.choices) + max_per_column - 1) // max_per_column
            for i, choice in enumerate(self.choices):
                col = i // max_per_column
                row = i % max_per_column
                # x and y position for this choice
                choice_x = x + self.padding + col * (self.width // num_columns)
                choice_y = line_y + row * (self.font.get_height() + self.choice_spacing)
                # highlight the selected choice
                if i == self.selected:
                    prefix = "X "
                    color = (255, 255, 120)
                else:
                    prefix = " "
                    color = (200, 200, 200)
                surf = self.font.render(prefix + choice, True, color)
                screen.blit(surf, (choice_x, choice_y))
