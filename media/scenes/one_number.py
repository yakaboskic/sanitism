"""One number, six outputs: the sanitism.dev hero video.

A value lives once in manifest.yaml and a sentence in docs/results.md uses
it. One build prints it into LaTeX, PDF, Word, interactive HTML, a slide deck
and a blog post. Then the value changes once, and every output follows.

Text only (no MathTex), so rendering needs manim and ffmpeg but no LaTeX.
Render it the way the README describes; the page plays site/media/one-number.*.
"""

from manim import (  # type: ignore[import-not-found]
    DOWN,
    LEFT,
    RIGHT,
    UP,
    UL,
    AnimationGroup,
    Arrow,
    BackgroundRectangle,
    Circle,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    RoundedRectangle,
    Scene,
    ShowPassingFlash,
    Text,
    Transform,
    VGroup,
    config,
)

config.background_color = "#172033"

INK = "#172033"  # page ink, the video's background
PANEL = "#22304d"  # source panels: the inside
PAPER = "#f6f8f7"  # output cards: the outside
LIGHT = "#e6eaf0"
MUTED = "#8d9ab0"
KEY = "#9fc0ec"  # YAML keys, ballpoint blue lifted for a dark ground
MARKER = "#ffe14d"  # highlighter: a number that knows its source
LINES = "#cfd6df"

MONO, SERIF = "Menlo", "Charter"
OLD, NEW = "12,453", "12,618"


def code_line(text: str, indent: int, colors: dict[str, str], size: int = 21) -> Text:
    line = Text(text, font=MONO, font_size=size, color=LIGHT, t2c=colors)
    line.indent = indent  # type: ignore[attr-defined]
    return line


def stack(lines: list[Text], gap: float = 0.13) -> VGroup:
    """Lay code lines out top to bottom, indenting by character width."""
    char = Text("M", font=MONO, font_size=21).width
    group = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=gap)
    left = group.get_left()[0]
    for line in lines:
        line.shift(RIGHT * (left + line.indent * char - line.get_left()[0]))  # type: ignore[attr-defined]
    return group


def panel(title: str, body: VGroup, width: float) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.14, width=width, height=body.height + 1.0,
        fill_color=PANEL, fill_opacity=1, stroke_width=0,
    )
    label = Text(title, font=MONO, font_size=17, color=MUTED)
    label.move_to(box.get_corner(UL) + RIGHT * (label.width / 2 + 0.3) + DOWN * 0.32)
    body.next_to(label, DOWN, aligned_edge=LEFT, buff=0.24)
    return VGroup(box, label, body)


def marked(value: str, font: str, size: int) -> VGroup:
    number = Text(value, font=font, font_size=size, color=INK, weight="BOLD")
    mark = BackgroundRectangle(number, color=MARKER, fill_opacity=1, buff=0.07)
    return VGroup(mark, number)


def card(kind: str, value: str) -> VGroup:
    """A small page standing in for one output, with the number highlighted."""
    w, h = 2.55, 1.62
    page = RoundedRectangle(corner_radius=0.08, width=w, height=h, fill_color=PAPER, fill_opacity=1, stroke_width=0)
    title = Text(kind, font=SERIF, font_size=19, color="#4f5a6d")
    title.move_to(page.get_corner(UL) + RIGHT * (title.width / 2 + 0.18) + DOWN * 0.24)
    parts = VGroup(page, title)
    if kind == "HTML":  # a browser window's three dots
        dots = VGroup(*[Circle(radius=0.04, fill_color=LINES, fill_opacity=1, stroke_width=0) for _ in range(3)])
        dots.arrange(RIGHT, buff=0.07).move_to(page.get_corner(UP + RIGHT) + LEFT * 0.36 + DOWN * 0.22)
        parts.add(dots)
    if kind == "Word":  # the header band of a Word page
        band = Rectangle(width=w - 0.36, height=0.05, fill_color=KEY, fill_opacity=1, stroke_width=0)
        band.next_to(title, DOWN, buff=0.1, aligned_edge=LEFT)
        parts.add(band)
    font = MONO if kind == "LaTeX" else SERIF
    size = 34 if kind == "Slides" else 28
    number = marked(value, font, size)
    number.move_to(page.get_center() + DOWN * 0.08)
    if kind != "Slides":  # body text around the number
        for dy, frac in ((-0.5, 0.78), (-0.66, 0.52)):
            bar = Line(LEFT * w * frac / 2, RIGHT * w * frac / 2, stroke_width=3, color=LINES)
            bar.move_to(page.get_center() + UP * dy).align_to(title, LEFT)
            parts.add(bar)
    parts.add(number)
    parts.number = number  # type: ignore[attr-defined]
    return parts


class OneNumber(Scene):
    def construct(self) -> None:
        # Inside: the manifest and the markdown that uses it
        value_line = code_line(f"value: {OLD.replace(',', '')}", 4, {"value:": KEY, OLD.replace(",", ""): MARKER})
        manifest_lines = [
            code_line("variables:", 0, {"variables:": KEY}),
            code_line("n_samples:", 2, {"n_samples:": KEY}),
            value_line,
            code_line("source: data/qc.csv", 4, {"source:": KEY}),
            code_line("command: python qc.py", 4, {"command:": KEY}),
        ]
        manifest = panel("manifest.yaml", stack(manifest_lines), width=5.45)
        md_lines = [
            code_line("We analyzed {{n_samples:,}}", 0, {"{{n_samples:,}}": MARKER}),
            code_line("samples after QC.", 0, {}),
        ]
        markdown = panel("docs/results.md", stack(md_lines), width=5.45)
        inside = VGroup(manifest, markdown).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        inside.to_edge(LEFT, buff=0.55).shift(UP * 0.25)

        # Outside: six outputs from one build
        kinds = ["LaTeX", "PDF", "Word", "HTML", "Slides", "Blog"]
        cards = VGroup(*[card(k, OLD) for k in kinds]).arrange_in_grid(rows=3, cols=2, buff=(0.28, 0.28))
        cards.to_edge(RIGHT, buff=0.55).shift(UP * 0.25)

        arrow = Arrow(
            inside.get_right() + RIGHT * 0.15, cards.get_left() + LEFT * 0.15,
            buff=0, stroke_width=5, color=KEY, max_tip_length_to_length_ratio=0.18,
        )
        build = Text("build", font=MONO, font_size=20, color=KEY).next_to(arrow, UP, buff=0.14)

        caption = Text("One number, six outputs.", font=SERIF, font_size=30, color=LIGHT)
        caption.to_edge(DOWN, buff=0.42)

        # 1. the source
        self.play(FadeIn(manifest[0]), FadeIn(manifest[1]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.15) for line in manifest_lines], lag_ratio=0.18), run_time=1.3)
        self.play(FadeIn(markdown, shift=UP * 0.1), run_time=0.7)
        self.wait(0.3)

        # 2. one build, every output
        self.play(GrowArrow(arrow), FadeIn(build), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cards], lag_ratio=0.14), run_time=1.5)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=0.5)
        self.wait(1.6)

        # 3. change it once
        new_value = code_line(f"value: {NEW.replace(',', '')}", 4, {"value:": KEY, NEW.replace(",", ""): MARKER})
        new_value.move_to(value_line, aligned_edge=LEFT)
        self.play(Transform(value_line, new_value), run_time=0.6)
        self.play(Indicate(value_line, color=MARKER, scale_factor=1.08), run_time=0.6)
        flash = arrow.copy().set_color(MARKER)
        self.play(ShowPassingFlash(flash, time_width=0.6), run_time=0.7)
        swaps = []
        for c in cards:
            old = c.number  # type: ignore[attr-defined]
            new = marked(NEW, old[1].font, int(old[1].font_size)).move_to(old)
            swaps.append(Transform(old, new))
        self.play(AnimationGroup(*swaps), run_time=0.8)
        self.play(LaggedStart(*[Indicate(c.number, color=MARKER, scale_factor=1.12) for c in cards], lag_ratio=0.05), run_time=0.9)  # type: ignore[attr-defined]
        self.play(Transform(caption, Text("Change it once. Every output follows.", font=SERIF, font_size=30, color=LIGHT).move_to(caption)), run_time=0.6)
        self.wait(2.2)

        # 4. clear the stage so the loop starts clean
        self.play(FadeOut(VGroup(inside, arrow, build, cards, caption)), run_time=0.7)
        self.wait(0.2)
