## pygame-oto
Rhythm game written in pygame, python

## Requirements
- `Python3==3.9.13`
- `pygame==2.5.1`

## Run
clone this repo, then run `main.py`
```bash
python ./main.py
```

you can also run on web with pygbag
(requirement: `pygbag==0.7.2`)
```bash
pygbag ./main.py
```

## Play
in menu screen, F11 key to toggle fullscreen mode.
select score by mouse click.
in game screen, ESC key to quit game.

## Custom Score
```
├─scores
│  ├─fooo
│  │  │  config.json
│  │  │  fooo.mp3
│  │  │
│  │  └─notes
│  │          easy.csv
```
### `config.json`
```json
{
    "title": "<title>",
    "music_file": "fooo.mp3",
    "bpm": 60,
    "speed": 6,
    "lanes": {
        "easy": 3
    }
}
```
### `easy.csv`
`easy` is difficulty name.
give it the same name as you set in `config.json`
```csv
beat,lane
1,1
1.5,2
1.75,2
```