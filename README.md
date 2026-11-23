[![Bounty](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/juliocafefs/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/juliocafefs/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in One Day — 23 November 2026

Entry for the make.fun competition
[news-image-20261123](https://make.fun/bounty/news-image-20261123):
"Sum up 23 November's world news in one image."

The entry image is a newspaper front page for **Monday 23 November 2026**:

- **Lead** — Ukraine sinks the Russian corvette *Merkury* off Libya:
  President Zelensky confirmed seven Ukrainian naval drones sank the
  corvette at Benghazi, destroyed a Ka-27 helicopter and hit the weapons
  cargo ship MV *Angara*.
- **Indonesia** — the confirmed death toll from the fire at the PT Fonusa
  Agung Mulia candy factory in Cikande, Banten, rose to 24, with about
  30 workers still missing.
- **Markets** — the AI sell-off spread through Asia again: Seoul's KOSPI
  fell more than 5% intraday and Taiwan's short-sale ban took effect,
  while US futures rebounded.
- **Belgium** — a nationwide anti-austerity strike closed Belgian
  airspace from 07:00 to 21:00; nearly all flights were cancelled,
  affecting some 60,000 passengers at Brussels Airport.
- **India–Nepal** — PM Narendra Modi hosted Nepal's PM Balendra Shah in
  New Delhi with a ceremonial welcome and about 100 minutes of talks;
  an Ayodhya–Janakpur train service was announced.
- **Ukraine** — rescuers searched the flattened apartment block in
  Dymer, near Kyiv, after a Russian strike; at least 11 people were
  killed, and a 7-year-old boy was pulled alive from the rubble.
- **Also Monday** — the UN and the US condemned the drone strikes on
  Khartoum that damaged UN premises.

Every story was reported on 23 November 2026 and cross-checked against
at least two independent news reports before it was drawn.

## How it works

- `build_image.py` draws the front page with Python Pillow (shapes and
  text only, no external artwork) and writes `entry.png`
  (1024×1024, PNG).
- `main.ts` is the competition program: Node 22, standard library only,
  no network. It carries the finished PNG as base64 and writes it,
  byte for byte, to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).
  Running it twice produces identical output.

## License

MIT — see [LICENSE](LICENSE).
