from dataclasses import dataclass, field
from typing import Dict, List
from models.article import Article


@dataclass
class Corpus:
    articles: Dict[str, Article] = field(default_factory=dict)

    def add(self, article: Article, term: str):
        """
        Add article to corpus with deduplication.
        """
        if article.pmid not in self.articles:
            article.terms = [term]
            self.articles[article.pmid] = article
        else:
            existing = self.articles[article.pmid]
            if term not in existing.terms:
                existing.terms.append(term)

    def __len__(self):
        return len(self.articles)

    def get_all(self) -> List[Article]:
        return list(self.articles.values())

    def to_json(self) -> List[dict]:
        return [vars(article) for article in self.articles.values()]
