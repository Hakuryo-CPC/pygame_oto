import pygame
import time
import os

font_path = f"{os.getcwd()}/assets/font/RocknRollOne-Regular.ttf"


class JudgeText:
    def __init__(self, judge, lane):
        if judge and not judge == "none":
            self.judge = judge
        else:
            self.judge = ""
        self.lane = lane
        self.font = pygame.font.Font(font_path, 20)
        self.starttime = time.time()

    def count_time(self):
        if time.time() - self.starttime > 1:
            self.judge = ""

    def draw_judge(self, screen, lane_width):
        window_size = screen.get_size()
        judge_text = self.font.render(self.judge, True, (0, 0, 0))
        screen.blit(judge_text, (lane_width * (self.lane - 1), window_size[1] * 0.93))


class ComboText:
    def __init__(self, combo):
        self.combo = str(combo)
        self.font = pygame.font.Font(font_path, 20)
        self.starttime = time.time()

    def count_time(self):
        if time.time() - self.starttime > 1:
            self.combo = ""

    def draw_combo(self, screen):
        window_size = screen.get_size()
        combo_text = self.font.render(self.combo, True, (0, 0, 0))
        screen.blit(combo_text, (window_size[0] * 0.85, window_size[1] * 0.25))
