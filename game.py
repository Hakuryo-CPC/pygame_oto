import pygame
from pygame.locals import RESIZABLE
from pygame.locals import VIDEORESIZE
import json
import csv
import os
import time
from chardet import detect

from note import Note
from text import JudgeText
from text import ComboText

# Pygame Color Definitions
BG_COLOR = pygame.Color(200, 200, 200)
LINE_COLOR = pygame.Color(0, 0, 0)


class Game:
    def __init__(self, window_size, score_name, difficulty):
        self.window_size = window_size
        self.score_name = score_name
        self.difficulty = difficulty

        self.combo = 0
        self.notes = []
        self.music_playing = False

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(self.window_size, RESIZABLE)
        self.clock = pygame.time.Clock()

        self.load_score()

        pygame.mixer.music.load(self.music_path)

        # lane to judge_text but it's 0-indexed
        self.judge_texts = [JudgeText("none", 0)] * self.lanes
        self.combo_text = ComboText(0)
        self.starttime = time.time()
        # lane to last judged time but it's 0-indexed
        self.last_judged = [self.starttime] * self.lanes

        self.note_arrive_time = (self.window_size[1] * 0.9) / (self.speed * 60)
        self.music_starttime = self.starttime + self.note_arrive_time

        self.main_loop()

    def load_score(self):
        score_dir = f"{os.getcwd()}/scores/{self.score_name}/"
        config_path = score_dir + "config.json"
        notes_path = score_dir + f"notes/{self.difficulty}.csv"

        # detect file encoding for config
        with open(config_path, "rb") as bf:
            conf_binary_data = bf.read()
            conf_encode_data = detect(conf_binary_data)

        # load config
        with open(config_path, encoding=conf_encode_data["encoding"]) as f:
            config = json.load(f)
        self.lanes = config["lanes"][self.difficulty]
        self.speed = config["speed"]
        self.music_path = f"{score_dir}{config['music_file']}"

        # detect file encoding for notes
        with open(notes_path, "rb") as bf:
            notes_binary_data = bf.read()
            notes_encode_data = detect(notes_binary_data)

        self.note_list = []
        with open(notes_path, encoding=notes_encode_data["encoding"]) as f:
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
                        ),
                    ]
                )

    def main_loop(self):
        self.running = True
        while self.running:
            self.event()
            self.draw_board()
            self.draw_notes()
            self.play_music()

            pygame.display.flip()
            self.clock.tick(60)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == VIDEORESIZE:
                self.window_size = self.screen.get_size()

    def draw_notes(self):
        for note in self.note_list:
            if (
                abs(
                    time.time() - self.music_starttime + self.note_arrive_time - note[0]
                )
                < 0.03
            ):
                self.notes.append(note[1])
                self.note_list.remove(note)
        for note in self.notes:
            note.draw_note()
            self.judge(note)

    def judge(self, note):
        lane_to_key = {
            1: pygame.K_1,
            2: pygame.K_2,
            3: pygame.K_3,
            4: pygame.K_4,
            5: pygame.K_5,
        }

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[lane_to_key[note.lane]]:
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

        if note.is_fallen():
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
