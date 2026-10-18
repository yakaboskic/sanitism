# sanitism

Landing page for [sanitism.dev](https://sanitism.dev), the home of
[document-sanity](https://github.com/yakaboskic/document-sanity) and
[presentation-sanity](https://github.com/yakaboskic/presentation-sanity).

Built for autists to communicate their work, sanely.

`site/` is published to GitHub Pages by
[`.github/workflows/pages.yml`](.github/workflows/pages.yml) on every push to
`main`. The custom domain is set in the repo's Pages settings, so no `CNAME`
file is needed.

## Sources for the visuals

Everything on the page that isn't a screenshot is generated from a source in
this repo. Edit the source, then re-export:

| Output in `site/` | Source | How to rebuild |
|---|---|---|
| `figures/*.svg` | `figures/*.drawio` | open in draw.io, or `draw.io -x -f svg -b 16 -o site/figures/NAME.svg figures/NAME.drawio` |
| `media/one-number.mp4` and `-poster.jpg` | `media/scenes/one_number.py` (manim, no LaTeX needed) | see below |
| `shots/*.jpg` | the live demos and the template repo on GitHub | headless Chrome at 2x, cropped and saved as JPEG |

The figures use only system fonts (Georgia, Menlo), so they render the same
on this page and in a GitHub README.

Rendering the hero video (any environment with manim and ffmpeg):

```bash
manim -qh --fps 30 media/scenes/one_number.py OneNumber
ffmpeg -i media/videos/one_number/1080p30/OneNumber.mp4 -c:v libx264 -crf 25 -preset slow \
  -pix_fmt yuv420p -movflags +faststart -an site/media/one-number.mp4
ffmpeg -ss 6.6 -i media/videos/one_number/1080p30/OneNumber.mp4 -frames:v 1 -q:v 3 \
  site/media/one-number-poster.jpg
```

The highlighted numbers on the page (the files `init` writes, the test counts)
carry their provenance in `data-*` attributes; update them with each release.
