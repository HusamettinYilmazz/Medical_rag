from collections import defaultdict
from pubmed.pubmed_client import search, fetch
from pipeline.parser import parse
from utils.logger import get_logger
logger = get_logger("data_pipeline")

def run_pipeline(terms: list[str]):
    articles = {}
    total_fetched = 0
    errors = 0

    for term in terms:
        try:
            pmids = search(term)
            xml_data = fetch(pmids)
            parsed = parse(xml_data)

            total_fetched += len(parsed)

            added = 0
            updated = 0
            for art in parsed:
                pmid = art.pmid

                if not pmid:
                    continue

                if pmid not in articles:
                    art.terms = [term]
                    articles[pmid] = art
                    added += 1
                else:
                    articles[pmid].terms.append(term)
                    updated += 1

            logger.info(
            f"Term '{term}' processed successfully | "
            f"fetched={len(parsed)}, new={added}, updated={updated}"
        )
            
        except Exception as e:
            logger.error(f"Error with term '{term}': {e}")
            errors += 1

    unique_articles = len(articles)
    duplicates_removed = total_fetched - unique_articles

    summary = {
        "terms_processed": len(terms),
        "total_fetched": total_fetched,
        "unique_articles": unique_articles,
        "duplicates_removed": duplicates_removed,
        "errors": errors,
    }

    return list(articles.values()), summary
