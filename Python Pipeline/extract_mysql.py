import pandas as pd

from mysql_connection import get_mysql_connection
from logger_config import logger


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


def extract_table(table_name):

    connection = get_mysql_connection()

    try:

        query = f"SELECT * FROM {table_name}"

        df = pd.read_sql(query, connection)

        logger.info(
            f"Extracted {len(df)} rows from {table_name}"
        )

        return df

    except Exception as error:

        logger.error(
            f"Extraction failed for {table_name}: {error}"
        )

        raise

    finally:

        connection.close()


def extract_all_tables():

    extracted_data = {}

    for table in TABLES:

        df = extract_table(table)

        extracted_data[table] = df

    return extracted_data


if __name__ == "__main__":

    data = extract_all_tables()

    print("\nExtraction Summary")
    print("=" * 50)

    for table_name, df in data.items():

        print(
            f"{table_name:<25} {len(df):>6} rows"
        )