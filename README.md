# Front Page, Wednesday 25 November 2026

![Competition](https://make.fun/badge/news-image-20261125.svg)
![Rank](https://make.fun/badge/news-image-20261125/LuJialin12/news-image-20261125/rank.svg)
![Reward](https://make.fun/badge/news-image-20261125/LuJialin12/news-image-20261125/reward.svg)

Entry for the bounty [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125).

## What it is

A one-image newspaper front page (1024x1024 PNG) summing up the world news of
Wednesday 25 November 2026:

- Two oil tankers hit naval mines in the Strait of Hormuz
- Houthi strike on a Saudi refinery and on Riyadh
- New US tariffs
- Huawei guilty verdict
- Solomon Islands-Australia pact
- Pakistan's first astronaut aboard Shenzhou-24

## How to run

Python 3.13, standard library only, no network:

```
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This copies the bundled `entry.png` byte for byte to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default output directory: `/output`). Every run writes identical bytes.

## License

MIT, see [LICENSE](LICENSE).
