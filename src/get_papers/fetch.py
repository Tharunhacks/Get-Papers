from typing import List, Dict
from Bio import Entrez

Entrez.email = "your.email@example.com"  # Replace with your real email

def search_ids(query: str, retmax: int = 200) -> List[str]:
    with Entrez.esearch(db="pubmed", term=query, retmax=retmax) as handle:
        result = Entrez.read(handle)
    return result["IdList"]

def fetch_articles(pmids: List[str]) -> List[Dict]:
    with Entrez.efetch(db="pubmed", id=",".join(pmids), retmode="xml") as handle:
        records = Entrez.read(handle)
    return records["PubmedArticle"]
