import pygame
import os

from state import State


class Result:
    def __init__(self, screen, point):
        self.screen = screen
        self.point = point

        self.next_state = State.Result

        font_path = f"{os.getcwd()}/assets/font/RocknRollOne-Regular.ttf"
        self.font = pygame.font.Font(font_path, 50)

    def main_loop(self):
        self.event()
        self.draw_result()

        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = State.Quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.judge_click(event.pos)

    def draw_result(self):
        self.screen.fill((200, 200, 200))

        point_text = self.font.render(f"スコア: {self.point}", True, (0, 0, 0))
        self.screen.blit(
            point_text,
            (self.screen.get_size()[0] * 0.4, self.screen.get_size()[1] * 0.4),
        )

        menu_text = self.font.render("Menuに戻る", True, (0, 0, 0))
        self.menu_text_rect = menu_text.get_rect(
            topleft=(self.screen.get_size()[0] * 0.4, self.screen.get_size()[1] * 0.6)
        )
        self.screen.blit(menu_text, self.menu_text_rect)

    def judge_click(self, pos):
        if self.menu_text_rect.collidepoint(pos):
            self.next_state = State.Menu
