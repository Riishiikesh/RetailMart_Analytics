import os

from dotenv import load_dotenv
from google.cloud import bigquery

from process_data import process_all_tables
from logger_config import logger


load_dotenv()


PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BIGQUERY_DATASET")


TABLES = [
    "categories",
    "customers",
    "products",
    "sales_transactions",
    "sales_items",
    "vouchers",
    "voucher_redemptions",
    "returns"
]


def load_table_to_bigquery(
    client,
    table_name,
    dataframe
):

    table_id = (
        f"{PROJECT_ID}."
        f"{DATASET_ID}."
        f"{table_name}"
    )


    job_config = bigquery.LoadJobConfig(

        write_disposition=(
            bigquery.WriteDisposition
            .WRITE_TRUNCATE
        ),

        autodetect=True
    )


    logger.info(
        f"Starting BigQuery load: {table_id}"
    )


    try:

        load_job = client.load_table_from_dataframe(
            dataframe,
            table_id,
            job_config=job_config
        )


        load_job.result()


        table = client.get_table(table_id)


        logger.info(
            f"Loaded {table.num_rows} rows "
            f"into {table_id}"
        )


        return table.num_rows


    except Exception as error:

        logger.error(
            f"BigQuery load failed for "
            f"{table_name}: {error}"
        )

        raise

def main():

    logger.info("=" * 60)
    logger.info("BIGQUERY LOAD STARTED")
    logger.info("=" * 60)


    client = bigquery.Client(
        project=PROJECT_ID
    )


    processed_data = process_all_tables()


    results = {}


    for table_name in TABLES:

        dataframe = processed_data[table_name]


        source_count = len(dataframe)


        target_count = load_table_to_bigquery(
            client,
            table_name,
            dataframe
        )


        if source_count != target_count:

            raise ValueError(
                f"Row count mismatch for {table_name}: "
                f"source={source_count}, "
                f"target={target_count}"
            )


        logger.info(
            f"Row count validation passed: "
            f"{table_name}"
        )


        results[table_name] = target_count


    logger.info("=" * 60)
    logger.info("BIGQUERY LOAD COMPLETED")
    logger.info("=" * 60)


    print("\nBigQuery Load Summary")
    print("=" * 50)


    for table_name, row_count in results.items():

        print(
            f"{table_name:<25} "
            f"{row_count:>6} rows"
        )


if __name__ == "__main__":

    main()