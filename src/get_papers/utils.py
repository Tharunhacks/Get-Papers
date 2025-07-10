import csv
from typing import Iterable, Tuple, List

def save_csv(rows: Iterable[Tuple], filename: str) -> None:
    header = [
        "PubmedID", "Title", "Publication Date",
        "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            row = list(row)
            row[3] = "; ".join(row[3])  # authors
            row[4] = "; ".join(row[4])  # affiliations
            writer.writerow(row)
