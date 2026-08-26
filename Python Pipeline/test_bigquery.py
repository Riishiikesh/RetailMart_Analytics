import os

from dotenv import load_dotenv
from google.cloud import bigquery


load_dotenv()


project_id = os.getenv("GCP_PROJECT_ID")


client = bigquery.Client(
    project=project_id
)


print(
    "Connected to BigQuery project:",
    client.project
)