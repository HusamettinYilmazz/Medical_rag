import xml.etree.ElementTree as ET
from models.article import Article

def get_text(element, path):
    found = element.find(path)
    return found.text if found is not None else None


def parse(xml_data: str) -> list[dict]:
    if not xml_data:
        return []

    root = ET.fromstring(xml_data)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        medline = article.find("MedlineCitation")
        article_data = medline.find("Article") if medline is not None else None

        pmid = get_text(medline, "PMID")
        title = get_text(article_data, "ArticleTitle")

        abstract_parts = article_data.findall(".//AbstractText") if article_data is not None else []
        abstract = " ".join([a.text for a in abstract_parts if a.text]) if abstract_parts else None

        journal = get_text(article_data, "Journal/Title")
        year = get_text(article_data, "Journal/JournalIssue/PubDate/Year")

        # first author
        author = None
        author_list = article_data.findall(".//Author") if article_data is not None else []
        if author_list:
            last = get_text(author_list[0], "LastName")
            first = get_text(author_list[0], "ForeName")
            if last and first:
                author = f"{first} {last}"

        # DOI
        doi = None
        for el in article.findall(".//ArticleId"):
            if el.attrib.get("IdType") == "doi":
                doi = el.text

        articles.append(
            Article(
            pmid= pmid,
            title= title,
            abstract= abstract,
            authors= author,
            journal= journal,
            year= year,
            doi= doi,
            terms= []
            ))

    return articles