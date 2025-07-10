from typing import List, Tuple
import re

def scan_article(article_xml) -> Tuple[str, str, str, List[str], List[str], str]:
    art = article_xml["MedlineCitation"]["Article"]

    pmid = article_xml["MedlineCitation"]["PMID"]
    title = art["ArticleTitle"]
    date = art["Journal"]["JournalIssue"]["PubDate"].get("Year", "")

    non_acad_names = []
    company_names = []

    for author in art.get("AuthorList", []):
        aff = author.get("AffiliationInfo", [{}])[0].get("Affiliation", "")
        if aff and not re.search(r"univ|college|dept|school|hospital", aff, re.I):
            if re.search(r"pharma|bio|therapeutics|inc|gmbh|ltd|llc", aff, re.I):
                name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()
                non_acad_names.append(name)
                company_names.append(aff)

    if not non_acad_names:
        raise ValueError("No qualifying author found")

    # Find first email in affiliations
    email = ""
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", " ".join(company_names))
    if match:
        email = match.group(0)

    return pmid, title, date, non_acad_names, company_names, email
