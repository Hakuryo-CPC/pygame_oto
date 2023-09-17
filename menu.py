import pygame
import os
import json

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
        self.selecting_id = 2
        self.selecting_score = ""

        self.get_scores()
        # asyncio.run(self.main_loop())
        self.main_loop()

    def main_loop(self):
        self.running = True
        while self.running:
            self.event()
            self.draw_scores()

            pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = State.Quit
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.judge_click(event.pos)

    def judge_click(self, pos):
        for tr in self.text_rects:
            if tr[1].collidepoint(pos):
                self.selecting = self.scores[tr[0]]
                self.next_state = State.Game
                self.running = False

    def draw_scores(self):
        n = min(len(self.scores), 5)

        self.screen.fill((200, 200, 200))
        self.text_rects = []
        for i in range(n):
            color = (0, 0, 0)
            text = self.font.render(
                f"[{self.scores[i].difficulty}]{self.scores[i].title}", True, color
            )
            text_rect = text.get_rect(
                topleft=(self.window_size[0] * 0.2, self.window_size[1] * 0.2 * i)
            )
            self.text_rects.append([i, text_rect])
            self.screen.blit(text, text_rect)

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
