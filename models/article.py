from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Article:
    pmid: str
    title: str
    abstract: str
    authors: List[str]
    journal: str
    year: Optional[str]
    doi: Optional[str]
    terms: List[str]
