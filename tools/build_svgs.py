#!/usr/bin/env python3
"""Generate the "Corporate Weirdcore" SVG panels used by README.md.

Run from the repo root:  python3 tools/build_svgs.py
Output goes to assets/. Edit the CONTENT section below, then re-run.

Style rules (mirrors the portfolio's DESIGN.md): solid colors only, no
gradients, no rounded corners, no blur. Thick black borders, hard offset
shadows, serif display type against uppercase terminal mono.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

PAPER = "#F4F3ED"
INK = "#0C0C0C"
WHITE = "#FFFFFF"
BLUE = "#2945FF"
YELLOW = "#FFD700"

SERIF = "'Times New Roman', Times, 'Liberation Serif', 'Nimbus Roman', Georgia, serif"
MONO = "'Courier New', Courier, 'Liberation Mono', 'Nimbus Mono PS', monospace"


# ---------------------------------------------------------------- helpers

def mono_width(text: str, size: float, spacing: float) -> float:
    """Courier-family glyphs are 0.6em wide; add letter-spacing per glyph."""
    return len(text) * (size * 0.6 + spacing)


def t(x, y, text, *, size, font=MONO, fill=INK, weight="normal", spacing=0,
      anchor="start", italic=False, extra=""):
    style = "italic" if italic else "normal"
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
        f'font-weight="{weight}" font-style="{style}" letter-spacing="{spacing}" '
        f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(text)}</text>'
    )


def rect(x, y, w, h, *, fill="none", stroke=None, sw=0):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{s}/>'


def window_controls(right, bar_y, bar_h):
    """Three square OS buttons on the right of an ink title bar."""
    size = bar_h - 16
    y = bar_y + 8
    parts = []
    for i, glyph in enumerate(("min", "max", "close")):
        x = right - 12 - (3 - i) * (size + 6) + 6
        parts.append(rect(x, y, size, size, fill=INK, stroke=WHITE, sw=2))
        cx, cy, q = x + size / 2, y + size / 2, size / 4
        if glyph == "min":
            parts.append(f'<line x1="{cx-q}" y1="{cy+q}" x2="{cx+q}" y2="{cy+q}" stroke="{WHITE}" stroke-width="2"/>')
        elif glyph == "max":
            parts.append(rect(cx - q, cy - q, 2 * q, 2 * q, stroke=WHITE, sw=2))
        else:
            parts.append(f'<path d="M{cx-q} {cy-q}L{cx+q} {cy+q}M{cx+q} {cy-q}L{cx-q} {cy+q}" stroke="{WHITE}" stroke-width="2"/>')
    return "".join(parts)


def window(w, h, title, *, body=WHITE, shadow=8, bar_h=36, border=4):
    """A clunky OS window: hard shadow, thick border, ink title bar."""
    x = y = border / 2
    ww, wh = w - shadow - border, h - shadow - border
    return "".join([
        rect(x + shadow, y + shadow, ww, wh, fill=INK),
        rect(x, y, ww, wh, fill=body, stroke=INK, sw=border),
        rect(x, y, ww, bar_h, fill=INK),
        t(x + 18, y + bar_h / 2 + 5, title, size=13, fill=WHITE, weight="bold", spacing=3),
        window_controls(x + ww, y, bar_h),
    ])


def svg(w, h, inner, label, style=""):
    css = f"<style>{style}</style>" if style else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">'
        f'<title>{escape(label)}</title>{css}{inner}</svg>\n'
    )


def tag(x, y, text, *, size=11, spacing=1.5, fill=WHITE, color=INK, pad=8, h=24):
    w = mono_width(text, size, spacing) + pad * 2
    return w, rect(x, y, w, h, fill=fill, stroke=INK, sw=2) + t(
        x + pad, y + h / 2 + size * 0.35, text, size=size, fill=color,
        weight="bold", spacing=spacing)


def write(name, content):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", OUT / name)


# ---------------------------------------------------------------- CONTENT

HEADER = {
    "bar": "C:\\DZAKY\\DOSSIER.EXE",
    "file": "FILE NO. 2636 — PERSONNEL RECORD",
    "name": ("Dzaky Fatur", "Rahman"),
    "role": "SOFTWARE ENGINEER // FULLSTACK · AI · MULTI-TENANT SAAS",
    "stats": [
        ("CLASS", "Software Eng."),
        ("MAIN", "TypeScript / Rust"),
        ("SPEC", "RAG · SaaS"),
        ("BASE", "Tangerang, ID"),
        ("LANG", "ID / EN"),
        ("XP", "~1.5 YRS"),
    ],
}

BUTTONS = [
    ("btn-portfolio.svg", "PORTFOLIO ↗", True),
    ("btn-linkedin.svg", "LINKEDIN ↗", False),
    ("btn-email.svg", "EMAIL ↗", False),
    ("btn-cv.svg", "CV.PDF ↓", False),
]

SECTIONS = [
    ("sec-about.svg", "01", "About", "ABOUT.TXT"),
    ("sec-projects.svg", "02", "Selected Work", "LEVELS.DAT"),
    ("sec-stack.svg", "03", "Inventory", "STACK.SYS"),
]

PROJECTS = [
    {
        "file": "proj-chatrigo.svg", "level": "01", "exe": "CHATRIGO.EXE",
        "title": "Chatrigo", "kind": "MULTI-TENANT AI CHATBOT SAAS",
        "lines": [
            "Omnichannel chatbot platform unifying WhatsApp,",
            "Instagram, Telegram, LINE and web chat into",
            "per-tenant workspaces, with a RAG-grounded",
            "AI sales agent.",
        ],
        "tags": ["NESTJS", "NEXT.JS", "POSTGRES", "REDIS", "TEMPORAL"],
        "link": "chatrigo.id ↗",
    },
    {
        "file": "proj-replygo.svg", "level": "02", "exe": "REPLYGO.EXE",
        "title": "ReplyGo", "kind": "LINK-IN-BIO STOREFRONT",
        "lines": [
            "Storefront for creators and small sellers:",
            "catalog, QRIS checkout, shipping checks,",
            "branded invoices and an AI assistant that",
            "answers buyers before checkout.",
        ],
        "tags": ["RUST", "AXUM", "PGVECTOR", "REACT"],
        "link": "replygo.id ↗",
    },
    {
        "file": "proj-egov.svg", "level": "03", "exe": "EGOV_BPN.EXE",
        "title": "E-Gov Balikpapan", "kind": "3 MUNICIPAL SYSTEMS · ALL LIVE",
        "lines": [
            "E-Sign: QR-stamped document signing across",
            "278 schools. E-KGB: salary review and",
            "promotion workflows. E-Manuntung: Flutter",
            "public-service app for citizens.",
        ],
        "tags": ["LARAVEL", "TAILWIND", "QUEUES", "FLUTTER"],
        "link": "edocument.balikpapan.go.id ↗",
    },
    {
        "file": "proj-its.svg", "level": "04", "exe": "THESIS.EXE",
        "title": "Adaptive ITS", "kind": "UNDERGRADUATE THESIS",
        "lines": [
            "Intelligent tutoring system with AI agents",
            "for real-time feedback and adaptive support,",
            "gamified on the Octalysis framework.",
        ],
        "tags": ["AI AGENTS", "OCTALYSIS", "EDTECH"],
        "link": "github.com/dzaky2636 ↗",
    },
]

# (label, [tags]); tags in HIGHLIGHT get the yellow accent.
STACK = [
    ("LANG", ["TYPESCRIPT", "RUST", "GO", "PHP", "PYTHON", "SQL"]),
    ("FRONT", ["NEXT.JS", "REACT", "ASTRO", "SVELTE", "TAILWIND", "FLUTTER"]),
    ("BACK", ["NODE.JS", "NESTJS", "AXUM", "LARAVEL", "PRISMA", "TEMPORAL"]),
    ("DATA", ["POSTGRESQL", "PGVECTOR", "REDIS", "SUPABASE"]),
    ("AI", ["RAG PIPELINES", "EMBEDDINGS", "LLM ORCHESTRATION", "OPENROUTER"]),
    ("INFRA", ["DOCKER", "RAILWAY", "VERCEL", "S3", "GIT"]),
]
HIGHLIGHT = {"TYPESCRIPT", "RUST", "RAG PIPELINES", "POSTGRESQL"}

FOOTER_LEFT = "EOF ■ NO GRADIENTS. NO ROUNDED CORNERS. NO SOFT SHADOWS."
FOOTER_RIGHT = "© 2026 DZAKY FATUR RAHMAN"


# ---------------------------------------------------------------- builders

def build_header():
    W, H = 1000, 350
    h = HEADER
    parts = [window(W, H, h["bar"], body=PAPER)]

    # file label on a yellow strip
    fw = mono_width(h["file"], 13, 4) + 16
    parts.append(rect(28, 62, fw, 26, fill=YELLOW, stroke=INK, sw=2))
    parts.append(t(36, 80, h["file"], size=13, weight="bold", spacing=4))

    # massive serif name, blinking blue full stop
    parts.append(t(28, 178, h["name"][0], size=96, font=SERIF, spacing=-2))
    parts.append(
        f'<text x="28" y="268" font-family="{SERIF}" font-size="96" '
        f'letter-spacing="-2" fill="{INK}">{escape(h["name"][1])}'
        f'<tspan class="blink" fill="{BLUE}">.</tspan></text>'
    )
    parts.append(f'<line x1="28" y1="290" x2="620" y2="290" stroke="{INK}" stroke-width="3"/>')
    parts.append(t(28, 318, h["role"], size=13, weight="bold", spacing=2.5))

    # STATS.DAT inventory block
    bx, by, bw, bh = 660, 66, 300, 248
    parts.append(rect(bx + 6, by + 6, bw, bh, fill=INK))
    parts.append(rect(bx, by, bw, bh, fill=WHITE, stroke=INK, sw=3))
    parts.append(rect(bx, by, bw, 30, fill=BLUE, stroke=INK, sw=3))
    parts.append(t(bx + 14, by + 20, "STATS.DAT", size=12, fill=WHITE, weight="bold", spacing=3))
    parts.append(t(bx + bw - 14, by + 20, "LV.99", size=12, fill=YELLOW, weight="bold", spacing=2, anchor="end"))
    for i, (k, v) in enumerate(h["stats"]):
        y = by + 62 + i * 34
        parts.append(t(bx + 16, y, k, size=13, weight="bold", spacing=2))
        parts.append(t(bx + bw - 16, y, v, size=13, spacing=0.5, anchor="end"))
        if i < len(h["stats"]) - 1:
            parts.append(f'<line x1="{bx+16}" y1="{y+12}" x2="{bx+bw-16}" y2="{y+12}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 4"/>')

    css = ".blink{animation:b 1.1s steps(1) infinite}@keyframes b{50%{opacity:0}}"
    write("header.svg", svg(W, H, "".join(parts), "Dzaky Fatur Rahman — Software Engineer", css))


def build_buttons():
    W, H, S = 240, 64, 6
    for name, label, primary in BUTTONS:
        fill, color = (BLUE, WHITE) if primary else (WHITE, INK)
        inner = (
            rect(2 + S, 2 + S, W - S - 4, H - S - 4, fill=INK)
            + rect(2, 2, W - S - 4, H - S - 4, fill=fill, stroke=INK, sw=3)
            + t((W - S) / 2, (H - S) / 2 + 6, label, size=16, fill=color,
                weight="bold", spacing=3, anchor="middle")
        )
        write(name, svg(W, H, inner, label.rstrip(" ↗↓")))


def build_sections():
    W, H, S = 1000, 72, 6
    for name, num, title, file in SECTIONS:
        bw, bh = W - S - 4, H - S - 4
        inner = (
            rect(2 + S, 2 + S, bw, bh, fill=INK)
            + rect(2, 2, bw, bh, fill=PAPER, stroke=INK, sw=4)
            + rect(2, 2, 76, bh, fill=INK)
            + t(40, bh / 2 + 9, num, size=24, fill=WHITE, weight="bold", anchor="middle")
            + t(100, bh / 2 + 13, title, size=38, font=SERIF, italic=True, spacing=-1)
            + t(bw - 20, bh / 2 + 7, file, size=13, weight="bold", spacing=4, anchor="end")
        )
        write(name, svg(W, H, inner, title))


def build_projects():
    W, H = 490, 320
    for p in PROJECTS:
        parts = [window(W, H, f"LEVEL {p['level']} // {p['exe']}")]
        kw = mono_width(p["kind"], 11, 2.5) + 14
        parts.append(rect(22, 54, kw, 22, fill=YELLOW, stroke=INK, sw=2))
        parts.append(t(29, 69, p["kind"], size=11, weight="bold", spacing=2.5))
        parts.append(t(22, 124, p["title"], size=44, font=SERIF, spacing=-1))
        for i, line in enumerate(p["lines"]):
            parts.append(t(22, 156 + i * 23, line, size=17, font=SERIF))
        x = 22
        for name in p["tags"]:
            w, el = tag(x, 250, name)
            parts.append(el)
            x += w + 6
        parts.append(t(456, 298, p["link"], size=12, fill=BLUE, weight="bold", spacing=1, anchor="end"))
        write(p["file"], svg(W, H, "".join(parts), f"{p['title']} — {' '.join(p['lines'])}"))


def build_stack():
    W, row_h, top = 1000, 48, 62
    H = top + len(STACK) * row_h + 28
    parts = [window(W, H, "INVENTORY.SYS — EQUIPPED ITEMS")]
    for i, (label, items) in enumerate(STACK):
        y = top + i * row_h
        parts.append(t(28, y + 20, label, size=14, weight="bold", spacing=3))
        x = 130
        for item in items:
            hl = item in HIGHLIGHT
            w, el = tag(x, y, item, size=14, pad=10, fill=YELLOW if hl else WHITE, h=32)
            parts.append(el)
            x += w + 8
    label = "Stack: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in STACK)
    write("stack.svg", svg(W, H, "".join(parts), label))


def build_footer():
    W, H = 1000, 48
    inner = (
        rect(0, 0, W, H, fill=INK)
        + t(20, 29, FOOTER_LEFT, size=12, fill=PAPER, weight="bold", spacing=2)
        + t(W - 20, 29, FOOTER_RIGHT, size=12, fill=YELLOW, weight="bold", spacing=2, anchor="end")
    )
    write("footer.svg", svg(W, H, inner, "End of file"))


if __name__ == "__main__":
    build_header()
    build_buttons()
    build_sections()
    build_projects()
    build_stack()
    build_footer()
