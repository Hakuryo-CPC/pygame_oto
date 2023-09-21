import pygame
from pygame import RESIZABLE
import asyncio

from menu import Menu
from game import Game
from state import State
from result import Result

WINDOW_SIZE = (1280, 720)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)


async def main():
    state = State.Menu
    menu = Menu(screen)

    running = True
    while running:
        if state == State.Menu:
            menu.main_loop()
            state = menu.next_state
            if state == State.Game:
                score = menu.selecting.name
                difficulty = menu.selecting.difficulty
                game = Game(screen, score, difficulty)

        elif state == State.Game:
            game.main_loop()
            state = game.next_state
            if state == State.Result:
                result = Result(screen, game.point)

        elif state == State.Result:
            result.main_loop()
            state = result.next_state
            if state == State.Menu:
                menu = Menu(screen)

        elif state == State.Quit:
            running = False

        await asyncio.sleep(0)


asyncio.run(main())
