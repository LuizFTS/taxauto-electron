import re
from typing import List


def detect_header_from_lines(lines: List[str]) -> int:
    """
    Detect header using both delimiter density and semantic content.
    """

    if not lines:
        raise ValueError("File is empty.")

    parsed_lines = [line.split(";") for line in lines]

    # Calcula a mediana de campos para identificar linhas "ricas"
    field_counts = [len([c for c in cols if c.strip()]) for cols in parsed_lines]
    median_fields = sorted(field_counts)[len(field_counts) // 2]

    scores = []
    for idx, cols in enumerate(parsed_lines):
        cleaned = [c.strip() for c in cols if c.strip()]
        if not cleaned:
            scores.append((idx, 0))
            continue

        # Penaliza linhas com muito menos campos que a mediana (ex: linha de título)
        field_density = len(cleaned) / max(median_fields, 1)
        if field_density < 0.5:
            scores.append((idx, 0))
            continue

        unique_ratio = len(set(cleaned)) / len(cleaned)

        text_cells = [
            c
            for c in cleaned
            if not c.replace(",", "").replace(".", "").replace("-", "").replace("/", "").isdigit()
        ]
        text_ratio = len(text_cells) / len(cleaned)

        # Penaliza linhas onde campos parecem ser datas ou valores isolados
        date_like = sum(1 for c in cleaned if re.match(r"\d{2}/\d{2}/\d{4}", c))
        date_penalty = 1 - (date_like / len(cleaned))

        score = len(cleaned) * text_ratio * unique_ratio * field_density * date_penalty
        scores.append((idx, score))

    best_idx, _ = max(scores, key=lambda x: x[1])
    return best_idx
