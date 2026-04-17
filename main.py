import os

import json
from dataclasses import asdict
from pipeline.data_pipeline import run_pipeline

from models.corpus import Corpus
from models.article import Article
from models.enums import RetrievalMethod
from controllers.retrieval_controller import RetrievalController
from services.bm25_service import BM25Service
from services.semantic_service import SemanticService
from services.rrf_service import RRFService

from evals.eval import Evaluator


from utils.config import get_settings
settings = get_settings()
from utils.logger import get_logger
logger = get_logger("main")

terms = [
    "atrial fibrillation",
    "type 2 diabetes mellitus",
    "pediatric asthma management",
    "acute otitis media",
    "chronic kidney disease",
    "iron deficiency anemia",
    "community acquired pneumonia",
    "gestational diabetes",
    "celiac disease diagnosis",
    "allergic rhinitis treatment"
]


def run_ingestion():
    logger.info("Running ingestion pipeline")

    articles, summary = run_pipeline(terms)

    logger.info(f"Articles collected: {len(articles)}")

    os.makedirs(os.path.dirname(settings.ARTICLES_OUTPUT_PATH), exist_ok=True)
    with open(settings.ARTICLES_OUTPUT_PATH, "w") as f:
        json.dump([asdict(a) for a in articles], f, indent=2)

    logger.info(f"Saved to {settings.ARTICLES_OUTPUT_PATH}")

    for k, v in summary.items():
        logger.info(f"{k}: {v}")

    return articles, summary

def load_articles():
    if not os.path.exists(settings.ARTICLES_OUTPUT_PATH):
        run_ingestion()
    
    logger.info("Loading articles from disk")

    with open(settings.ARTICLES_OUTPUT_PATH, "r") as f:
        data = json.load(f)

    logger.info(f"Loaded {len(data)} articles")

    # If needed: convert dict → Article dataclass
    return [Article(**a) for a in data]

def build_retriever(articles):
    logger.info("Building retrieval system")

    corpus = Corpus()
    for a in articles:
        corpus.add(a, "ingestion")

    bm25_service = BM25Service(corpus)
    semantic_service = SemanticService(corpus, settings.EMBEDDING_MODEL)
    rrf_service = RRFService()

    retriever = RetrievalController(
        bm25_service,
        semantic_service,
        rrf_service
    )

    logger.info("Retriever ready")

    return retriever

def run_retrieval_tests(retriever):
    logger.info("Running retrieval tests")

    test_queries = [
        "What are the latest guidelines for managing type 2 diabetes?",
        "Çocuklarda akut otitis media tedavisi nasıl yapılır?",
        "iron deficiency anemia pregnancy treatment",
        "Çölyak hastalığı tanı kriterleri nelerdir?",
        "Antibiotic resistance patterns in community acquired pneumonia"
    ]

    retrieval_method = RetrievalMethod(
        settings.RETRIEVAL_METHOD
        if settings.RETRIEVAL_METHOD
        else settings.DEFAULT_RETRIEVAL_METHOD
    )

    logger.info(f"Retrieval method: {retrieval_method.value}")

    for query in test_queries:
        logger.info(f"\nQuery: {query}")

        results = retriever.search(query, retrieval_method)

        for r in results[:5]:
            logger.info(f"- {r['article'].title} | score={r['score']}")

def run_evaluation(retriever):
    logger.info("Running evaluation")
    model_name = settings.EMBEDDING_MODEL
    evaluator = Evaluator(retriever, model_name=model_name)

    test_queries = [
        "What are the latest guidelines for managing type 2 diabetes?",
        "Çocuklarda akut otitis media tedavisi nasıl yapılır?",
        "iron deficiency anemia pregnancy treatment",
        "Çölyak hastalığı tanı kriterleri nelerdir?",
        "Antibiotic resistance patterns in community acquired pneumonia"
    ]

    results = evaluator.evaluate_all(test_queries)

    logger.info("\n=== EVALUATION RESULTS ===")

    for r in results:
        logger.info(r)

def main():
    logger.info("Starting Medical RAG Pipeline")

    # 1. Data ingestion
    articles = load_articles()

    # 2. Build retrieval system
    retriever = build_retriever(articles)

    # 3. Run retrieval demo
    run_retrieval_tests(retriever)

    # 4. Run evaluation
    run_evaluation(retriever)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()