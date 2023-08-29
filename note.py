import pygame

class Note:
    def __init__(self, speed, lane, lane_width, screen):
        self.speed = speed
        self.lane = lane
        self.lane_width = lane_width
        self.screen = screen
        self.window_size = screen.get_size()

        self.x = (lane - 1) * lane_width
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, lane_width, 50)

    def draw_note(self):
        self.rect = self.rect.move(0, self.speed)
        self.error = abs( ((self.rect.top + self.rect.bottom) / 2) - self.window_size[1]*0.9 )
        pygame.draw.rect(self.screen, "red", self.rect, width=0)

    def judge(self):
        if self.error < 60*0.05*self.speed:
            return "perfect"
        elif self.error < 60*0.1*self.speed:
            return "good"
        elif self.error < 60*0.15*self.speed:
            return "ok"
        elif self.error < 60*0.35*self.speed:
            return "miss"
        else:
            return "none"

    def is_fallen(self):
        if self.rect.top > self.window_size[1]*0.9 + 60*0.25*self.speed:
            return True
        else:
            return False