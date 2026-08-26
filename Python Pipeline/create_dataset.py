import os

from dotenv import load_dotenv
from google.cloud import bigquery

from logger_config import logger


load_dotenv()


PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BIGQUERY_DATASET")


def create_dataset():

    client = bigquery.Client(
        project=PROJECT_ID
    )


    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"


    dataset = bigquery.Dataset(
        dataset_ref
    )


    dataset.location = "US"


    client.create_dataset(
        dataset,
        exists_ok=True
    )


    logger.info(
        f"BigQuery dataset ready: {dataset_ref}"
    )


if __name__ == "__main__":

    create_dataset()