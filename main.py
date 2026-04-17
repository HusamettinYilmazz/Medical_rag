import json
from dataclasses import asdict
from pipeline.data_pipeline import run_pipeline
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


def main():
    logger.info("Starting Medical RAG Data pipeline")
    articles, summary = run_pipeline(terms)

    with open(settings.ARTICLES_OUTPUT_PATH, "w") as f:
        json.dump([asdict(a) for a in articles], f, indent=2)

    logger.info("\nSummary:")
    for k, v in summary.items():
        logger.info(f"{k}: {v}")


if __name__ == "__main__":
    main()