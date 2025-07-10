import argparse, sys
from rich.console import Console
from get_papers.fetch import search_ids, fetch_articles
from get_papers.filter import scan_article
from get_papers.utils import save_csv

console = Console()

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma/biotech authors.")
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("-d", "--debug", action="store_true", help="Show debug logs")
    parser.add_argument("-f", "--file", help="Save output to CSV file")
    args = parser.parse_args()

    if args.debug:
        console.log(f"Searching for: {args.query}")

    try:
        pmids = search_ids(args.query)
    except Exception as e:
        console.print(f"[red]Failed to search PubMed:[/] {e}")
        sys.exit(1)

    rows = []
    for article in fetch_articles(pmids):
        try:
            rows.append(scan_article(article))
        except Exception:
            continue

    if not rows:
        console.print("[yellow]No matching results.")
        return

    if args.file:
        save_csv(rows, args.file)
        console.print(f"[green]Saved {len(rows)} rows to {args.file}")
    else:
        for row in rows:
            console.print(row)

if __name__ == "__main__":
    main()
