import pygame
import asyncio
import os

from state import State


class Result:
    def __init__(self, screen):
        self.screen = screen

        self.next_state = State.Result

        font_path = f"{os.getcwd()}/assets/font/RocknRollOne-Regular.ttf"
        self.font = pygame.font.Font(font_path, 50)

        asyncio.run(self.main_loop())

    async def main_loop(self):
        self.running = True
        while self.running:
            self.event()
            self.draw_result()

            pygame.display.flip()

            await asyncio.sleep(0)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = State.Quit
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.judge_click(event.pos)

    def draw_result(self):
        self.screen.fill((200, 200, 200))
        text = self.font.render("Menuに戻る", True, (0, 0, 0))
        self.text_rect = text.get_rect(
            topleft=(self.screen.get_size()[0] * 0.4, self.screen.get_size()[1] * 0.4)
        )
        self.screen.blit(text, self.text_rect)

    def judge_click(self, pos):
        if self.text_rect.collidepoint(pos):
            self.next_state = State.Menu
            self.running = False
