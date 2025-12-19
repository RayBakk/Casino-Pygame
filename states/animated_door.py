import pygame

class AnimatedDoor:
    def __init__(self, sheet_path, pos, frames_count=9, delay=50):
        self.sheet = pygame.image.load(sheet_path).convert_alpha()

        self.frames_count = frames_count
        self.frame_w = self.sheet.get_width() // frames_count
        self.frame_h = self.sheet.get_height()

        self.frames = []
        for i in range(frames_count):
            rect = pygame.Rect(i * self.frame_w, 0, self.frame_w, self.frame_h)
            self.frames.append(self.sheet.subsurface(rect).copy())

        self.frame = 0
        self.timer = 0
        self.delay = delay

        self.rect = pygame.Rect(pos[0], pos[1], self.frame_w, self.frame_h)

    def update(self, should_open):
        now = pygame.time.get_ticks()
        if now - self.timer >= self.delay:
            self.timer = now
            if should_open and self.frame < self.frames_count - 1:
                self.frame += 1
            elif not should_open and self.frame > 0:
                self.frame -= 1

    def draw(self, screen):
        screen.blit(self.frames[self.frame], self.rect.topleft)
