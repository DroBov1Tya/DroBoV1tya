#!/usr/bin/env python3
"""Render the profile artwork into assets/.

Run from the repository root: python3 tools/build_assets.py

Everything is a self-contained SVG, because GitHub shows README images through
<img>: no scripts, no external fonts, no foreignObject. Motion is CSS only, so
`prefers-reduced-motion` can switch it off; every element's resting state is
the finished picture, and keyframes only hide it on the way there.
"""

from __future__ import annotations

import random
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# The "dusk" palette shared with the site and Dusk Code. One accent only.
PANEL = "#13141f"
CARD = "#1b1c2a"
RAISED = "#262839"
TEXT = "#efedf7"
SOFT = "#aeadc4"
MUTED = "#8f8ea8"
HAIRLINE = "rgba(239,237,247,.09)"
ACCENT = "#b4a0f8"
STAR = "#dcd6ff"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
MONO_ADVANCE = 0.6  # glyph advance of the usual monospace faces, in em

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def pct(seconds: float, period: float) -> str:
    return f"{max(0.0, min(100.0, seconds / period * 100)):.3f}%"


def svg(width: int, height: int, title: str, style: str, body: str, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{escape(title)}">\n'
        f"<title>{escape(title)}</title>\n"
        f"<defs>{defs}</defs>\n"
        f"<style>{style}{REDUCED_MOTION}</style>\n"
        f"{body}\n</svg>\n"
    )


def sky_defs(width: int, height: int, clip_radius: int) -> str:
    """The violet night sky of the site's hero: a vertical wash plus a glow rising from below."""
    return (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0b0b16"/><stop offset=".6" stop-color="#14132a"/>'
        '<stop offset="1" stop-color="#1a1630"/></linearGradient>'
        '<radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" '
        f'gradientTransform="translate({width / 2} {height * 1.08}) scale({width * 1.2} {height * 0.7})">'
        '<stop offset="0" stop-color="rgb(130,90,230)" stop-opacity=".2"/>'
        '<stop offset=".7" stop-color="rgb(130,90,230)" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="frame"><rect width="{width}" height="{height}" rx="{clip_radius}"/></clipPath>'
    )


def stars(rng: random.Random, count: int, width: int, height: int, keep_clear=None) -> str:
    """Scatter stars, denser towards the top; about a third of them twinkle."""
    out = []
    while len(out) < count:
        x = rng.uniform(8, width - 8)
        y = 6 + (height - 12) * rng.random() ** 1.6
        if keep_clear and keep_clear(x, y):
            continue
        radius = rng.choice([0.6, 0.7, 0.8, 0.9, 1.0, 1.3])
        opacity = rng.uniform(0.35, 0.9)
        twinkle = ""
        if rng.random() < 0.35:
            twinkle = (
                f' class="tw" style="animation-duration:{rng.uniform(3.2, 7.0):.1f}s;'
                f'animation-delay:-{rng.uniform(0, 7):.1f}s"'
            )
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{STAR}" opacity="{opacity:.2f}"{twinkle}/>'
        )
    return "\n".join(out)


TWINKLE_CSS = ".tw{animation:tw 5s ease-in-out infinite}@keyframes tw{50%{opacity:.12}}"


# --------------------------------------------------------------------------- header


def header() -> str:
    width, height = 900, 300
    rng = random.Random(7)
    left = 56

    def over_text(x: float, y: float) -> bool:
        return 40 < x < 640 and 100 < y < 245

    # Role line: three phrases typed in turn. Each glyph sits in its own cell, so the
    # typing never depends on how wide a particular monospace face happens to be.
    phrases = [
        ("Application Security Engineer", 0.4, 0.055, 5.2),
        ("Rust developer", 5.9, 0.07, 9.6),
        ("Finding what breaks, building what holds", 10.3, 0.05, 15.5),
    ]
    period = 16.0
    glyph_window = 6.0  # a glyph stays lit this long; its phrase group hides it sooner
    size = 22
    advance = size * MONO_ADVANCE
    role_x, role_y = left + 26, 232

    css = [
        TWINKLE_CSS,
        f".g{{animation:g {period}s step-end infinite}}"
        f"@keyframes g{{0%{{opacity:1}}{pct(glyph_window, period)}{{opacity:0}}100%{{opacity:0}}}}",
        ".blink{animation:blink 1.1s step-end infinite}@keyframes blink{50%{opacity:0}}",
        f".shoot{{animation:shoot 14s linear infinite}}"
        "@keyframes shoot{0%,89%{opacity:0;transform:translate(0,0)}90%{opacity:.9}"
        "96%,100%{opacity:0;transform:translate(230px,72px)}}",
        ".draw{animation:draw .9s ease-out both}@keyframes draw{from{stroke-dashoffset:1}}",
    ]
    role = []
    caret_frames = [(0.0, 0)]
    for index, (phrase, start, per_glyph, end) in enumerate(phrases):
        fade = end + 0.3
        css.append(
            f".p{index}{{animation:p{index} {period}s linear infinite}}"
            f"@keyframes p{index}{{0%,{pct(start - 0.01, period)}{{opacity:0}}"
            f"{pct(start, period)},{pct(end, period)}{{opacity:1}}"
            f"{pct(fade, period)},100%{{opacity:0}}}}"
        )
        glyphs = []
        for i, char in enumerate(phrase):
            typed_at = start + i * per_glyph
            caret_frames.append((typed_at, i + 1))
            if char == " ":
                continue
            glyphs.append(
                f'<text class="g" x="{role_x + (i + 0.5) * advance:.1f}" y="{role_y}" '
                f'style="animation-delay:{typed_at - period:.3f}s">{escape(char)}</text>'
            )
        caret_frames.append((fade, 0))
        resting = "1" if index == 0 else "0"
        role.append(f'<g class="p{index}" opacity="{resting}">{"".join(glyphs)}</g>')

    caret_css = "".join(
        f"{pct(at, period)}{{transform:translateX({cells * advance:.1f}px)}}" for at, cells in caret_frames
    )
    css.append(f".caret{{animation:caret {period}s step-end infinite}}@keyframes caret{{{caret_css}}}")
    resting_caret = len(phrases[0][0]) * advance

    # Scutum, "the shield": a real constellation, and a quiet nod to the day job.
    shield = [(742, 70), (810, 94), (792, 172), (722, 150)]
    lines = []
    for i, (x1, y1) in enumerate(shield):
        x2, y2 = shield[(i + 1) % len(shield)]
        lines.append(
            f'<line class="draw" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" pathLength="1" '
            f'stroke-dasharray="1" style="animation-delay:{0.8 + i * 0.7:.1f}s"/>'
        )
    shield_stars = "".join(
        f'<circle class="tw" cx="{x}" cy="{y}" r="{r}" fill="{STAR}" '
        f'style="animation-duration:{d}s;animation-delay:-{i}s"/>'
        for i, ((x, y), r, d) in enumerate(zip(shield, [2.2, 1.7, 2.0, 1.6], [6.5, 5.2, 7.1, 5.8]))
    )

    body = f"""<g clip-path="url(#frame)">
<rect width="{width}" height="{height}" fill="url(#sky)"/>
<rect width="{width}" height="{height}" fill="url(#glow)"/>
{stars(rng, 90, width, height, over_text)}
<g class="shoot" opacity="0"><line x1="330" y1="22" x2="386" y2="39.5" stroke="url(#trail)" stroke-width="1.4" stroke-linecap="round"/></g>
<g stroke="{ACCENT}" stroke-opacity=".42" stroke-width="1">{"".join(lines)}</g>
{shield_stars}
<text x="766" y="212" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="1.6" fill="{MUTED}">SCUTUM · THE SHIELD</text>
<text x="{left}" y="112" font-family="{MONO}" font-size="13" letter-spacing="2.4" fill="{ACCENT}">RIGA, LATVIA</text>
<text x="{left - 3}" y="184" font-family="{SANS}" font-size="68" font-weight="680" letter-spacing="-2" fill="{TEXT}">Neil Ermak</text>
<text x="{left}" y="{role_y}" font-family="{MONO}" font-size="{size}" fill="{ACCENT}">&gt;</text>
<g font-family="{MONO}" font-size="{size}" fill="{SOFT}" text-anchor="middle">{"".join(role)}</g>
<g class="caret" style="transform:translateX({resting_caret:.1f}px)"><rect class="blink" x="{role_x + 2}" y="{role_y - 19}" width="11" height="24" rx="1.5" fill="{ACCENT}"/></g>
</g>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="17.5" fill="none" stroke="{HAIRLINE}"/>"""
    defs = sky_defs(width, height, 18) + (
        '<linearGradient id="trail" gradientUnits="userSpaceOnUse" x1="330" y1="22" x2="386" y2="39.5">'
        f'<stop offset="0" stop-color="{STAR}" stop-opacity="0"/><stop offset="1" stop-color="{STAR}"/></linearGradient>'
    )
    title = (
        "Neil Ermak, Riga, Latvia. Application Security Engineer and Rust developer: "
        "finding what breaks, building what holds."
    )
    return svg(width, height, title, "".join(css), body, defs)


# --------------------------------------------------------------------------- whoami


def whoami() -> str:
    width = 640
    size, line_height = 15, 25
    advance = size * MONO_ADVANCE
    left, top = 30, 78
    period = 60.0
    fade_out = 58.2

    focus = [
        ("offensive security", "web apps and APIs · Active Directory · Linux"),
        ("vulnerability focus", "business-logic flaws · authentication bypass · injections"),
        ("backend", "async services · database design · containerized deployment"),
        ("tooling", "MCP servers and automation for AI-assisted security testing"),
    ]

    css = [".blink{animation:blink 1.1s step-end infinite}@keyframes blink{50%{opacity:0}}"]
    parts = []
    counter = 0

    def appear(at: float, markup: str, soft: bool = False) -> None:
        """Show `markup` from `at` until the loop fades out; soft elements ease in."""
        nonlocal counter
        name = f"a{counter}"
        counter += 1
        ease = 0.35 if soft else 0.0
        css.append(
            f".{name}{{animation:{name} {period}s linear infinite}}"
            f"@keyframes {name}{{0%,{pct(at, period)}{{opacity:0}}"
            f"{pct(at + ease + 0.001, period)},{pct(fade_out, period)}{{opacity:1}}"
            f"{pct(fade_out + 0.8, period)},100%{{opacity:0}}}}"
        )
        parts.append(f'<g class="{name}">{markup}</g>')

    caret_frames = []
    row = 0
    clock = 0.5

    def y_of(r: float) -> float:
        return top + r * line_height

    def prompt(command: str, per_glyph: float) -> None:
        nonlocal clock, row
        y = y_of(row)
        appear(clock, f'<text x="{left}" y="{y}" fill="{ACCENT}">$</text>')
        caret_frames.append((clock, 2, row))
        clock += 0.5
        for i, char in enumerate(command):
            at = clock + i * per_glyph
            caret_frames.append((at, 2 + i + 1, row))
            if char != " ":
                appear(
                    at,
                    f'<text x="{left + (2 + i + 0.5) * advance:.1f}" y="{y}" text-anchor="middle" fill="{TEXT}">{escape(char)}</text>',
                )
        clock += len(command) * per_glyph + 0.35
        row += 1

    prompt("whoami", 0.09)
    appear(
        clock,
        f'<text x="{left}" y="{y_of(row)}" fill="{TEXT}">Neil Ermak'
        f'<tspan fill="{MUTED}"> · </tspan><tspan fill="{SOFT}">application security engineer, Rust developer</tspan></text>',
        soft=True,
    )
    row += 1.6
    clock += 0.8

    prompt("cat focus.txt", 0.075)
    for label, value in focus:
        appear(
            clock,
            f'<text x="{left}" y="{y_of(row)}" fill="{ACCENT}"># {escape(label)}</text>'
            f'<text x="{left}" y="{y_of(row + 1)}" fill="{SOFT}">{escape(value)}</text>',
            soft=True,
        )
        clock += 0.45
        row += 2.25
    row += 0.2
    clock += 0.2

    last_row = row
    appear(clock, f'<text x="{left}" y="{y_of(last_row)}" fill="{ACCENT}">$</text>')
    caret_frames.append((clock, 2, last_row))
    height = int(y_of(last_row) + 30)

    def caret_at(cells: float, r: float) -> str:
        return f"translate({cells * advance:.1f}px,{r * line_height:.1f}px)"

    frames = [f"0%{{opacity:0;transform:{caret_at(2, 0)}}}"]
    frames += [f"{pct(at, period)}{{opacity:1;transform:{caret_at(c, r)}}}" for at, c, r in caret_frames]
    frames.append(f"{pct(fade_out + 0.8, period)},100%{{opacity:0;transform:{caret_at(2, last_row)}}}")
    css.append(f".caret{{animation:caret {period}s step-end infinite}}@keyframes caret{{{''.join(frames)}}}")

    body = f"""<rect width="{width}" height="{height}" rx="14" fill="{PANEL}"/>
<path d="M0 14a14 14 0 0 1 14-14h{width - 28}a14 14 0 0 1 14 14v26H0z" fill="{CARD}"/>
<rect y="40" width="{width}" height="1" fill="{HAIRLINE}"/>
<g fill="{RAISED}"><circle cx="24" cy="20" r="5.5"/><circle cx="43" cy="20" r="5.5"/><circle cx="62" cy="20" r="5.5"/></g>
<text x="{width / 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">neil@riga: ~</text>
<g font-family="{MONO}" font-size="{size}" xml:space="preserve">
{chr(10).join(parts)}
<g class="caret" style="transform:{caret_at(2, last_row)}"><rect class="blink" x="{left}" y="{top - 13}" width="8.5" height="17" rx="1" fill="{ACCENT}"/></g>
</g>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="13.5" fill="none" stroke="{HAIRLINE}"/>"""
    title = "Terminal. whoami: Neil Ermak, application security engineer, Rust developer. " + " ".join(
        f"{label.capitalize()}: {value.replace(' · ', ', ')}." for label, value in focus
    )
    return svg(width, height, title, "".join(css), body)


# --------------------------------------------------------------------------- project cards

# Each motif is drawn in a 40x40 box with the accent stroke; its animation classes are below.
MOTIFS = {
    "dusk": (
        '<path d="M11 24a9 9 0 0 1 18 0"/><path d="M6 24h28"/>'
        '<path class="m-a" d="M11 29h18"/><path class="m-b" d="M15 34h10"/>'
    ),
    "radar": (
        '<circle cx="20" cy="20" r="2" fill="currentColor" stroke="none"/><circle cx="20" cy="20" r="7" opacity=".55"/>'
        '<circle cx="20" cy="20" r="13" opacity=".3"/><circle class="m-ping" cx="20" cy="20" r="13" opacity="0"/>'
    ),
    "box": (
        '<rect x="7" y="11" width="18" height="18" rx="4"/><path d="M12 20h7" opacity=".55"/>'
        '<path class="m-flow" d="M25 20h10" stroke-dasharray="2.5 3"/><path d="M32 17l3 3-3 3"/>'
    ),
    "penta": (
        '<path d="M20 8 31.4 16.3 27 29.7H13L8.6 16.3z" opacity=".3"/>'
        + "".join(
            f'<circle class="m-node" cx="{x}" cy="{y}" r="2.2" fill="currentColor" stroke="none" style="animation-delay:{i}s"/>'
            for i, (x, y) in enumerate([(20, 8), (31.4, 16.3), (27, 29.7), (13, 29.7), (8.6, 16.3)])
        )
    ),
    "hook": (
        '<path d="M22 8v15a6 6 0 0 1-12 0v-2"/><path d="M7 24l3-3.5 3 3.5"/>'
        '<circle class="m-drop" cx="22" cy="8" r="2.2" fill="currentColor" stroke="none"/>'
        '<path d="M28 13h6M28 19h4" opacity=".45"/>'
    ),
    "chat": (
        '<path d="M8 12a4 4 0 0 1 4-4h16a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H18l-6 5v-5a4 4 0 0 1-4-4z"/>'
        + "".join(
            f'<circle class="m-dot" cx="{x}" cy="17" r="1.6" fill="currentColor" stroke="none" style="animation-delay:{d}s"/>'
            for x, d in [(14.5, 0), (20, 0.25), (25.5, 0.5)]
        )
    ),
    "morph": (
        '<path class="m-bar" d="M8 12h24" style="animation-delay:0s"/>'
        '<path class="m-bar m-bar2" d="M8 20h24" style="animation-delay:.3s"/>'
        '<path class="m-bar m-bar3" d="M8 28h24" style="animation-delay:.6s"/>'
    ),
    "grid": "".join(
        f'<rect class="m-cell" x="{x}" y="{y}" width="9" height="9" rx="2.5" style="animation-delay:{d}s"/>'
        for x, y, d in [(9, 9, 0), (22, 9, 1), (22, 22, 2), (9, 22, 3)]
    ),
}

MOTIF_CSS = (
    ".m-a{animation:m-fade 4s ease-in-out infinite}.m-b{animation:m-fade 4s ease-in-out -2s infinite}"
    "@keyframes m-fade{50%{opacity:.25}}"
    ".m-ping{transform-box:fill-box;transform-origin:center;animation:m-ping 3.6s ease-out infinite}"
    "@keyframes m-ping{0%{transform:scale(.15);opacity:.9}70%,100%{transform:scale(1.25);opacity:0}}"
    ".m-flow{animation:m-flow 1.6s linear infinite}@keyframes m-flow{to{stroke-dashoffset:-11}}"
    ".m-node{animation:m-node 5s ease-in-out infinite}@keyframes m-node{0%,24%,100%{opacity:.3}8%{opacity:1}}"
    ".m-drop{animation:m-drop 3.2s ease-in-out infinite}@keyframes m-drop{50%{opacity:.25}}"
    ".m-dot{animation:m-dot 1.6s ease-in-out infinite}@keyframes m-dot{0%,60%,100%{opacity:.3}30%{opacity:1}}"
    ".m-bar{transform-box:fill-box;transform-origin:left;animation:m-bar 6s ease-in-out infinite}"
    "@keyframes m-bar{0%,100%{transform:scaleX(1)}35%,60%{transform:scaleX(var(--messy,.55))}}"
    ".m-bar2{--messy:.85}.m-bar3{--messy:.35}"
    ".m-cell{animation:m-cell 4s ease-in-out infinite}@keyframes m-cell{0%,40%,100%{opacity:.3}15%{opacity:1}}"
)

PROJECTS = [
    {
        "file": "dusk-code",
        "name": "Dusk Code",
        "motif": "dusk",
        "featured": True,
        "lines": [
            "Open-source coding agent. One core with desktop,",
            "terminal and browser clients over one protocol; local",
            "history, any model provider, sandboxed plugins.",
        ],
        "stack": "RUST · SQLITE · MIT",
    },
    {
        "file": "aether",
        "name": "Aether",
        "motif": "radar",
        "lines": [
            "Self-hosted internet reconnaissance. Distributed",
            "agents run masscan, nmap, httpx, nuclei, tlsx and",
            "dnsx; results get a Shodan-style search with history.",
        ],
        "stack": "RUST · DOCKER",
    },
    {
        "file": "kali-mcp",
        "name": "kali-mcp",
        "motif": "box",
        "lines": [
            "A Kali Linux container for AI agents over MCP,",
            "behind a gateway: no NET_ADMIN or NET_RAW, and",
            "traffic leaves only through the SOCKS5 proxy.",
        ],
        "stack": "PYTHON · DOCKER",
    },
    {
        "file": "pentacore",
        "name": "PentaCore",
        "motif": "penta",
        "lines": [
            "Working memory for AI agents over MCP: goals,",
            "steps, attempts, findings and entities. One local",
            "binary, one SQLCipher file.",
        ],
        "stack": "RUST · SQLITE",
    },
    {
        "file": "rusty-hook",
        "name": "Rusty-Hook",
        "motif": "hook",
        "lines": [
            "Self-hosted webhook inspector, an alternative to",
            "webhook.site. Requests show up live over SSE;",
            "sign-in by admin key or OIDC.",
        ],
        "stack": "RUST · LEPTOS · POSTGRESQL",
    },
    {
        "file": "xbot",
        "name": "xbot",
        "motif": "chat",
        "lines": [
            "Telegram bot that sells VPN subscriptions on a",
            "Remnawave panel. Telegram Stars and CryptoBot",
            "payments; one process serves many bots.",
        ],
        "stack": "RUST · POSTGRESQL",
    },
    {
        "file": "dbmorph",
        "name": "DBMorph",
        "motif": "morph",
        "lines": [
            "Streaming converter for large, messy CSV, JSON,",
            "XLSX, SQL dumps, SQLite and Parquet. Detects",
            "encodings; flat memory for files larger than RAM.",
        ],
        "stack": "RUST",
    },
    {
        "file": "more",
        "name": "And the rest",
        "motif": "grid",
        "lines": [
            "hermes_auto, a Bash installer for a Hermes Agent",
            "security-assessment profile; Wifi-Scanner, a Wi-Fi",
            "scanner for single-board computers; and others.",
        ],
        "stack": "ALL REPOSITORIES",
    },
]


def card(project: dict) -> str:
    width, height = 410, 172
    featured = project.get("featured", False)
    border = f'stroke="{ACCENT}" stroke-opacity=".5"' if featured else f'stroke="{HAIRLINE}"'
    lines = "".join(
        f'<text x="22" y="{92 + i * 19}">{escape(line)}</text>' for i, line in enumerate(project["lines"])
    )
    body = f"""<rect width="{width}" height="{height}" rx="14" fill="{CARD}"/>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="13.5" fill="none" {border}/>
<rect x="22" y="20" width="40" height="40" rx="11" fill="{RAISED}"/>
<g transform="translate(22 20)" color="{ACCENT}" fill="none" stroke="{ACCENT}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{MOTIFS[project["motif"]]}</g>
<text x="76" y="47" font-family="{SANS}" font-size="20" font-weight="680" letter-spacing="-.3" fill="{TEXT}">{escape(project["name"])}</text>
<path d="M{width - 34} 45l10-10m-7 0h7v7" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<g font-family="{SANS}" font-size="13" fill="{SOFT}">{lines}</g>
<text x="22" y="{height - 19}" font-family="{MONO}" font-size="10.5" letter-spacing="1.3" fill="{MUTED}">{escape(project["stack"])}</text>"""
    title = f'{project["name"]}. {" ".join(project["lines"])} {project["stack"].title()}.'
    return svg(width, height, title, MOTIF_CSS, body)


# --------------------------------------------------------------------------- link buttons

GLYPHS = {
    "site": '<circle cx="8" cy="8" r="6.5"/><ellipse cx="8" cy="8" rx="2.8" ry="6.5"/><path d="M1.5 8h13"/>',
    "linkedin": (
        '<rect x="1.5" y="1.5" width="13" height="13" rx="3"/><path d="M5 7.2v4M8 11.2v-2.3a1.6 1.6 0 0 1 3.2 0v2.3M8 7.2v4"/>'
        '<circle cx="5" cy="4.9" r=".5" fill="currentColor"/>'
    ),
    "telegram": '<path d="M1.5 7.6 14.5 2l-2.4 12-4-3.6L14.5 2M8.1 10.4v3.4l1.9-1.7"/>',
    "channel": (
        '<circle cx="8" cy="8" r="1.4" fill="currentColor" stroke="none"/>'
        '<path d="M4.9 4.9a4.4 4.4 0 0 0 0 6.2M11.1 4.9a4.4 4.4 0 0 1 0 6.2M2.6 2.6a7.6 7.6 0 0 0 0 10.8M13.4 2.6a7.6 7.6 0 0 1 0 10.8"/>'
    ),
}

BUTTONS = [
    ("site", "Website", "Personal site"),
    ("linkedin", "LinkedIn", "LinkedIn"),
    ("telegram", "Telegram", "Telegram"),
    ("channel", "Channel", "Telegram channel"),
]


def button(glyph: str, label: str, title: str) -> str:
    size = 13
    text_width = len(label) * size * MONO_ADVANCE
    width, height = round(16 + 16 + 9 + text_width + 18), 38
    body = f"""<rect width="{width}" height="{height}" rx="10" fill="{CARD}"/>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="9.5" fill="none" stroke="{HAIRLINE}"/>
<g transform="translate(16 11)" color="{ACCENT}" fill="none" stroke="{ACCENT}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{GLYPHS[glyph]}</g>
<text x="41" y="23.5" font-family="{MONO}" font-size="{size}" fill="{TEXT}" textLength="{text_width:.1f}" lengthAdjust="spacingAndGlyphs">{escape(label)}</text>"""
    return svg(width, height, title, "", body)


# --------------------------------------------------------------------------- footer


def footer() -> str:
    width, height = 900, 84
    rng = random.Random(23)

    def over_text(x: float, y: float) -> bool:
        return 300 < x < 600 and 28 < y < 60

    body = f"""<g clip-path="url(#frame)">
<rect width="{width}" height="{height}" fill="url(#sky)"/>
<rect width="{width}" height="{height}" fill="url(#glow)"/>
{stars(rng, 46, width, height, over_text)}
<text x="{width / 2}" y="47" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing=".6" fill="{SOFT}">drobov1tya.github.io<tspan fill="{ACCENT}">/persona</tspan></text>
</g>
<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="13.5" fill="none" stroke="{HAIRLINE}"/>"""
    return svg(width, height, "Personal site: drobov1tya.github.io/persona", TWINKLE_CSS, body, sky_defs(width, height, 14))


def main() -> None:
    outputs = {"header.svg": header(), "whoami.svg": whoami(), "footer.svg": footer()}
    for project in PROJECTS:
        outputs[f'card-{project["file"]}.svg'] = card(project)
    for glyph, label, title in BUTTONS:
        outputs[f"link-{glyph}.svg"] = button(glyph, label, title)
    ASSETS.mkdir(exist_ok=True)
    for name, content in outputs.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content.encode('utf-8'))} bytes")


if __name__ == "__main__":
    main()
