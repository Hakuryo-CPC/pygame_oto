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


class KeyBindText:
    def __init__(self, lane_to_key, screen):
        self.lane_to_key = lane_to_key
        self.screen = screen

        self.font = pygame.font.Font(font_path, 20)

        self.window_size = screen.get_size()
        self.lane_width = self.window_size[0] / len(self.lane_to_key)

    def draw(self):
        for lane, game_key in self.lane_to_key.items():
            key_bind_text = self.font.render(game_key.label, True, (0, 0, 0))
            self.screen.blit(
                key_bind_text,
                (self.lane_width * (lane - 1), self.window_size[1] * 0.9),
            )


class PointText:
    def __init__(self, screen, point):
        self.screen = screen
        self.point = point

        self.font = pygame.font.Font(font_path, 20)

        self.window_size = self.screen.get_size()

    def draw(self):
        text = self.font.render(f"スコア: {self.point}", True, (0, 0, 0))
        self.screen.blit(text, (self.window_size[0] * 0.05, self.window_size[1] * 0.05))
