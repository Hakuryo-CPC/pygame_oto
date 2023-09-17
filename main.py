import pygame
from pygame import RESIZABLE

from menu import Menu
from game import Game
from state import State
from result import Result

WINDOW_SIZE = (1280, 720)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, RESIZABLE)

state = State.Menu

running = True
while running:
    if state == State.Menu:
        menu = Menu(screen)
        state = menu.next_state
        score = menu.selecting.name
        difficulty = menu.selecting.difficulty
    elif state == State.Game:
        state = Game(screen, score, difficulty).next_state
    elif state == State.Result:
        state = Result(screen).next_state
    elif state == State.Quit:
        running = False
