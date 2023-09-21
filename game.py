import pygame
from pygame.locals import VIDEORESIZE
import json
import csv
import os
import time

from note import Note
from text import JudgeText
from text import ComboText
from text import KeyBindText
from text import PointText
from state import State

# Pygame Color Definitions
BG_COLOR = pygame.Color(200, 200, 200)
LINE_COLOR = pygame.Color(0, 0, 0)

FPS = 60


class GameKey:
    def __init__(self, key, label):
        self.key = key
        self.label = label


class Game:
    def __init__(self, screen, score_name, difficulty):
        self.screen = screen
        self.window_size = screen.get_size()
        self.score_name = score_name
        self.difficulty = difficulty

        self.next_state = State.Game

        self.combo = 0
        self.point = 0
        self.notes = []
        self.music_playing = False

        self.clock = pygame.time.Clock()

        self.load_score()
        self.key_bind()

        # mixer init
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_path)
        sound_path = f"{os.getcwd()}/assets/sound/press.ogg"
        self.press_se = pygame.mixer.Sound(sound_path)

        # lane to judge_text but it's 0-indexed
        self.judge_texts = [JudgeText("none", 0)] * self.lanes
        self.combo_text = ComboText(0)
        self.starttime = time.time()
        # lane to last judged time but it's 0-indexed
        self.last_judged = [self.starttime] * self.lanes
        # lane to isclicked but it's 0-indexed
        self.clicked = [False] * self.lanes

        self.note_arrive_time = (self.window_size[1] * 0.9) / (self.speed * 60)
        self.music_starttime = self.starttime + self.note_arrive_time

    def load_score(self):
        score_dir = f"{os.getcwd()}/scores/{self.score_name}/"
        config_path = score_dir + "config.json"
        notes_path = score_dir + f"notes/{self.difficulty}.csv"

        encodings = ["UTF-8-SIG", "utf-8", "shift_jis", "utf-16-le", "utf-16"]

        # load config
        for encoding in encodings:
            try:
                with open(config_path, encoding=encoding) as f:
                    config = json.load(f)
                self.lanes = config["lanes"][self.difficulty]
                self.speed = config["speed"]
                self.music_path = f"{score_dir}{config['music_file']}"

                # load notes
                self.note_list = []
                with open(notes_path, encoding=encoding) as f:
                    reader = csv.reader(f)
                    for note in reader:
                        if note[0] == "beat":
                            continue

                        note_time = 60 / config["bpm"] * (float(note[0]) - 1)
                        self.note_list.append(
                            [
                                note_time,
                                Note(
                                    self.speed,
                                    int(note[1]),
                                    self.window_size[0] / self.lanes,
                                    self.screen,
                                    FPS,
                                ),
                            ]
                        )

                self.last_note_time = self.note_list[-1][0]
                break
            except:
                print(f"file encoding is not {encoding}, retrying...")

    def main_loop(self):
        self.clicked = [False] * self.lanes
        self.event()
        self.draw_board()
        self.draw_notes()
        KeyBindText(self.lane_to_key, self.screen).draw()
        PointText(self.screen, self.point).draw()
        self.play_music()

        pygame.display.flip()
        self.clock.tick(FPS)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.next_state = State.Quit
            elif event.type == VIDEORESIZE:
                self.window_size = self.screen.get_size()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.judge_click(event.pos)
                self.play_se()
            elif event.type == pygame.KEYDOWN:
                self.play_se()

    def judge_click(self, pos):
        for i in range(self.lanes):
            if pos[0] < self.window_size[0] / self.lanes * (i + 1):
                self.clicked[i] = True

    def draw_notes(self):
        time_now = time.time()
        for note in self.note_list:
            if (
                abs(time_now - self.music_starttime + self.note_arrive_time - note[0])
                < 0.03
            ):
                self.notes.append(note[1])
                self.note_list.remove(note)
        for note in self.notes:
            note.draw_note()
            self.judge(note)

    # Bind like:
    # Lane: 1 2 3     4 5
    # Key : D F Space J K
    def key_bind(self):
        self.lane_to_key = {}
        mid = int(self.lanes / 2)
        if self.lanes % 2 == 1:
            self.lane_to_key[mid + 1] = GameKey(key=pygame.K_SPACE, label="Space")

        left_side = [
            GameKey(pygame.K_f, "F"),
            GameKey(pygame.K_d, "D"),
            GameKey(pygame.K_s, "S"),
        ]
        right_side = [
            GameKey(pygame.K_j, "J"),
            GameKey(pygame.K_k, "K"),
            GameKey(pygame.K_l, "L"),
        ]
        for i in range(mid):
            self.lane_to_key[mid - i] = left_side[i]
            self.lane_to_key[mid + 1 + (self.lanes % 2) + i] = right_side[i]

    def judge(self, note):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[self.lane_to_key[note.lane].key] or self.clicked[note.lane - 1]:
            judge = note.judge()
            if time.time() - self.last_judged[note.lane - 1] > 0.1:
                if not judge == "none":
                    if judge == "miss":
                        self.combo = 0
                    else:
                        self.combo += 1

                    self.notes.remove(note)

                    self.judge_texts[note.lane - 1] = JudgeText(note.judge(), note.lane)
                    self.combo_text = ComboText(self.combo)
                    self.last_judged[note.lane - 1] = time.time()

                    if judge == "perfect":
                        self.point += 100
                    elif judge == "good":
                        self.point += 80
                    elif judge == "ok":
                        self.point += 40

                    if self.combo >= 15:
                        self.point += self.combo * 10

                    if self.combo == 10:
                        self.point += 250
                    elif self.combo == 20:
                        self.point += 500
                    elif self.combo == 50:
                        self.point += 1000
                    elif self.combo == 100:
                        self.point += 3000
        elif note.is_fallen():
            self.combo = 0
            self.notes.remove(note)
            self.judge_texts[note.lane - 1] = JudgeText("miss", note.lane)
            self.combo_text = ComboText(self.combo)

        # draw judge
        for j in self.judge_texts:
            j.count_time()
            j.draw_judge(self.screen, self.window_size[0] / self.lanes)

        # draw combo
        self.combo_text.count_time()
        self.combo_text.draw_combo(self.screen)

    def draw_board(self):
        # draw background
        self.screen.fill(BG_COLOR)

        # draw lines
        # [0] is judge line, others are lane line
        line_positions = [
            [
                [0, self.window_size[1] * 0.9],
                [self.window_size[0], self.window_size[1] * 0.9],
            ]
        ]
        lane_width = self.window_size[0] / self.lanes
        for i in range(self.lanes - 1):
            line_positions.append(
                [[(i + 1) * lane_width, 0], [(i + 1) * lane_width, self.window_size[1]]]
            )

        for pos in line_positions:
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                pygame.Vector2(pos[0][0], pos[0][1]),
                pygame.Vector2(pos[1][0], pos[1][1]),
                width=1,
            )

    def play_music(self):
        if (
            abs(time.time() - self.starttime - self.note_arrive_time) < 0.01
            and not self.music_playing
        ):
            self.music_starttime = time.time()
            pygame.mixer.music.play()
            self.music_playing = True

        if time.time() - self.music_starttime - self.last_note_time >= 1.5:
            self.next_state = State.Result

    def play_se(self):
        self.press_se.play()
        self.press_se.set_volume(1.0)
