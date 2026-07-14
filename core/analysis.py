import re
from collections import Counter

import plotly.graph_objects as go


def _words(text: str) -> list:

    return re.findall(r"\b\w+[’']?\w*\b", text.lower())


def _sentences(text: str) -> int:
    parts = [p.strip() for p in re.split(r"[.!?]+", text) if p.strip()]
    return max(1, len(parts))


def _words_per_sentence(text: str) -> float:
    return len(_words(text)) / _sentences(text)


def _avg_word_length(text: str) -> float:
    ws = _words(text)
    if not ws:
        return 0.0
    return sum(len(w) for w in ws) / len(ws)


def readability_label(text: str) -> str:
    # Heuristic readability label (no external heavy deps)
    wps = _words_per_sentence(text)
    awl = _avg_word_length(text)

    score = 206.835 - 1.015 * wps - 84.6 * awl  # rough Flesch-Kincaid-ish
    if score >= 90:
        return "Very Easy"
    if score >= 80:
        return "Easy"
    if score >= 60:
        return "Standard"
    if score >= 40:
        return "Difficult"
    return "Very Difficult"


def analyze_text(text: str):
    ws = _words(text)
    word_count = len(ws)
    char_count = len(text)

    label = readability_label(text)

    # char distribution chart (A-Z)
    letters = re.findall(r"[A-Za-z]", text)
    cnt = Counter([c.upper() for c in letters])
    letters_sorted = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    y = [cnt.get(ch, 0) for ch in letters_sorted]

    fig1 = go.Figure(data=go.Bar(x=letters_sorted, y=y))
    fig1.update_layout(
        template="plotly_dark",
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        title="Character Distribution (A-Z)",
    )

    # readability bar
    levels = ["Very Easy", "Easy", "Standard", "Difficult", "Very Difficult"]
    idx = levels.index(label) if label in levels else 2
    fig2 = go.Figure(
        data=go.Bar(x=levels, y=[1 if i == idx else 0 for i in range(len(levels))])
    )
    fig2.update_layout(
        template="plotly_dark",
        height=220,
        margin=dict(l=10, r=10, t=20, b=10),
        title="Readability Level",
        showlegend=False,
    )

    return {
        "word_count": word_count,
        "char_count": char_count,
        "readability_label": label,
        "charts": {"char_dist": fig1, "readability_bar": fig2},
    }

