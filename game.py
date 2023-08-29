import pygame

from note import Note
from text import JudgeText
from text import ComboText

# Pygame Color Definitions
BG_COLOR = pygame.Color(200, 200, 200)
LINE_COLOR = pygame.Color(0, 0, 0)

class Game:
    def __init__(self, window_size, lanes):
        self.window_size = window_size
        self.lanes = lanes

        self.combo = 0
        
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        self.judge_text = JudgeText("none", 1)
        self.combo_text = ComboText(0)

        self.main_loop()

    def main_loop(self):
        self.notes = []
        self.notes.append(Note(5, 3, self.window_size[0]/self.lanes, self.screen))
        self.running = True
        while self.running:
            self.event()
            self.draw_board()
            self.draw_notes()

            pygame.display.flip()
            self.clock.tick(60)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw_notes(self):
        for note in self.notes:
            note.draw_note()
            self.judge(note)
            
    def judge(self, note):
        lane_to_key = {1: pygame.K_d,
                       2: pygame.K_f,
                       3: pygame.K_SPACE,
                       4: pygame.K_j,
                       5: pygame.K_k}
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[lane_to_key[note.lane]] or note.is_fallen():
            judge = note.judge()
            if not judge == "none" or note.is_fallen():
                if judge == "miss":
                    self.combo = 0
                else:
                    self.combo += 1
                
                if note.is_fallen():
                    self.combo = 0

                self.notes.remove(note)
                self.notes.append(Note(5, 3, self.window_size[0]/self.lanes, self.screen))

                self.judge_text = JudgeText(note.judge(), note.lane)
                self.combo_text = ComboText(self.combo)

        # draw judge
        self.judge_text.count_time()
        self.judge_text.draw_judge(self.screen, self.window_size[0] / self.lanes)

        # draw combo
        self.combo_text.count_time()
        self.combo_text.draw_combo(self.screen)
                
    def draw_board(self):
        # draw background
        self.screen.fill(BG_COLOR)

        # draw lines
        line_positions = [[[0, self.window_size[1] * 0.9], [self.window_size[0], self.window_size[1]*0.9]]]
        lane_width = self.window_size[0] / self.lanes
        for i in range(self.lanes - 1):
            line_positions.append([[(i + 1) * lane_width, 0], [(i + 1) * lane_width, self.window_size[1]]])

        for pos in line_positions:
            pygame.draw.line(self.screen,
                             LINE_COLOR,
                             pygame.Vector2(pos[0][0], pos[0][1]),
                             pygame.Vector2(pos[1][0], pos[1][1]),
                             width = 1)