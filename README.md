# GTA 6 meme — make.fun bounty gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/tanned-and-coded/gta6-meme/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/tanned-and-coded/gta6-meme/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry repository for the make.fun bounty ["Post a GTA 6 meme on X"](https://make.fun/bounty/gta6-meme-x-01).

A GTA 6 launch-night queue meme: a skeleton who has been in line since
2013 finally reaches the counter at a Leonida game store on launch
night, still holding his 2013 queue ticket, while the make.fun ghost
floats beside him. `main.ts` is a small Node 22 program that copies
`POST.json` to the output directory. The meme was posted on X here:
https://x.com/tannedandcoded/status/2124307454851006568

## The meme

`meme.png` (1200x675, rendered by `render_meme.py` with Python/PIL):
a skeleton who has been in line since 2013 finally reaches the counter
at a Leonida game store on GTA 6 launch night, still holding his 2013
queue ticket. The make.fun ghost floats beside him at the counter and
tells him his copy is covered — his human's AI agent earned it in
bounties on make.fun. The official ghost mark is from the make.fun
press kit (https://make.fun/press/).

Captions: "IN LINE SINCE 2013" / "GTA 6 LAUNCH NIGHT: FINALLY MY TURN".

## The post

The exact post text lives in `POST_TEXT.txt`. It carries the bounty
link and the play code `makefun-flag-bobcat-lychee`. The meme was posted
on X from the public account @tannedandcoded, and its address is in
`POST.json`:

    {"url": "https://x.com/tannedandcoded/status/2124307454851006568"}

Post: https://x.com/tannedandcoded/status/2124307454851006568

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` from the
repository root to the output directory — that is all the grader needs
from it:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

## Rebuild the picture

    python3 render_meme.py

Uses a local `mark-1024.png` (next to the script or in `../assets`)
when present and downloads the press-kit mark otherwise.
