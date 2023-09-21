import pygame
import os
import json
from pygame.locals import VIDEORESIZE

from game import Game
from state import State


class Score:
    def __init__(self, name, title, difficulty):
        self.name = name
        self.title = title
        self.difficulty = difficulty


class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.window_size = self.screen.get_size()

        font_path = f"{os.getcwd()}/assets/font/RocknRollOne-Regular.ttf"
        self.font = pygame.font.Font(font_path, 50)

        self.next_state = State.Menu
        self.top = 0

        self.get_scores()
        # asyncio.run(self.main_loop())
        # self.main_loop()

    def main_loop(self):
        self.event()
        self.draw_scores()
        self.draw_scroll_button()

        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = State.Quit
            elif event.type == VIDEORESIZE:
                self.window_size = self.screen.get_size()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.judge_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

    def judge_click(self, pos):
        for tr in self.text_rects:
            if tr[1].collidepoint(pos):
                self.selecting = self.scores[tr[0] + self.top]
                self.next_state = State.Game

        if self.up_button.collidepoint(pos):
            self.top = max(0, self.top - 1)
        if self.down_button.collidepoint(pos):
            if self.top + 5 < len(self.scores):
                self.top += 1

    def draw_scores(self):
        n = min(len(self.scores), 5)

        self.screen.fill((200, 200, 200))
        self.text_rects = []
        for i in range(n):
            color = (0, 0, 0)
            text = self.font.render(
                f"[{self.scores[self.top + i].difficulty}]{self.scores[self.top + i].title}",
                True,
                color,
            )
            text_rect = text.get_rect(
                topleft=(
                    self.window_size[0] * 0.2,
                    self.window_size[1] * 0.12 + self.window_size[1] * 0.8 * 0.2 * i,
                )
            )
            self.text_rects.append([i, text_rect])
            self.screen.blit(text, text_rect)

    def draw_scroll_button(self):
        # up
        self.up_button = pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (
                self.window_size[0] * 0.2,
                self.window_size[1] * 0.02,
                self.window_size[0] * 0.4,
                self.window_size[1] * 0.1,
            ),
        )
        if not self.top == 0:
            pygame.draw.polygon(
                self.screen,
                (200, 200, 200),
                (
                    [self.window_size[0] * 0.4, self.window_size[1] * 0.04],
                    [self.window_size[0] * 0.35, self.window_size[1] * 0.1],
                    [self.window_size[0] * 0.45, self.window_size[1] * 0.1],
                ),
            )

        # down
        self.down_button = pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (
                self.window_size[0] * 0.2,
                self.window_size[1] * 0.87,
                self.window_size[0] * 0.4,
                self.window_size[1] * 0.1,
            ),
        )
        if self.top + 5 < len(self.scores):
            pygame.draw.polygon(
                self.screen,
                (200, 200, 200),
                (
                    [self.window_size[0] * 0.4, self.window_size[1] * 0.95],
                    [self.window_size[0] * 0.35, self.window_size[1] * 0.89],
                    [self.window_size[0] * 0.45, self.window_size[1] * 0.89],
                ),
            )

    def get_scores(self):
        score_dir = f"{os.getcwd()}/scores/"
        self.scores = []
        for score_name in os.listdir(score_dir):
            config_path = score_dir + score_name + "/config.json"

            encodings = ["UTF-8-SIG", "utf-8", "shift_jis", "utf-16-le", "utf-16"]

            for encoding in encodings:
                try:
                    with open(config_path, encoding=encoding) as f:
                        config = json.load(f)

                    for diff in config["lanes"]:
                        self.scores.append(
                            Score(
                                name=score_name, title=config["title"], difficulty=diff
                            )
                        )
                    break
                except:
                    print(f"{score_name} file encoding is not {encoding}, retrying...")
