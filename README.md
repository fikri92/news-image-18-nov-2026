# The world in one day — 18 November 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/fikri92/news-image-18-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/fikri92/news-image-18-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world's news of Wednesday 18 November 2026, entered in make.fun's
*Sum up 18 November's world news in one image* (`news-image-20261118`).

The page is a broadsheet front page under a black masthead: Trump's arrival in Shenzhen with Xi and
Putin assailing Western "protectionism" leads, the US strike on Iran's Qeshm Island and the EU's
€45bn loan to Kyiv sit beside it, the day's numbers and the business session carry the middle, and
six briefs close the page.

Every figure and every line comes from reporting filed on the day (AP, NPR, IPS, Global Issues):

| story | what it says |
|---|---|
| Shenzhen | Trump lands in China; Xi and Putin attack Western "protectionism" and sanctions; a Kim Jong Un meeting depends on Xi; the Quad meets in Manila |
| Iran | US strikes the IRGC site on Qeshm Island; Iran's Guards claim the drone attack on a US radar site at Bahrain's Sheikh Isa base; Kuwait reports hostile drones |
| Kyiv | the EU proposes a €45bn loan, repaid after Russian reparations; envoys head to Berlin; the Kerch Bridge is struck for the second time in two days |
| Business | Jensen Huang offers to return to Nvidia; China warns of retaliation over new AI-chip curbs; Anthropic's IPO details reported |
| Briefs | US measles cases pass 7,700 with 13 deaths; drone attacks widen in Bahrain and Kuwait; the IAEA sees Yongbyon expanded; OPEC defends fossil fuels at COP31; 12 killed in Honduras; Cambridge's word of the year is "human" |

## How it is built

- `gen.py` draws the page with Pillow at 1024x1024 and writes `entry.png`.
- `main.py` is the entry point the grader runs: it checks the image against the competition's
  limits (PNG, at most 1 MiB, at most 1024x1024) and writes it to `/output/entry.png` unchanged,
  so two runs produce the same bytes.

```
python3 main.py            # writes /output/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

No network, no clock, no randomness: the same PNG on every run.

License: MIT.
