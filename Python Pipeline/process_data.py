from extract_mysql import extract_all_tables

from transform import transform_data

from validation import (
    validate_columns,
    validate_not_empty,
    validate_duplicates,
    validate_null_primary_key
)

from config import PRIMARY_KEYS

from logger_config import logger


def process_all_tables():

    logger.info("=" * 60)
    logger.info("ETL PROCESS STARTED")
    logger.info("=" * 60)


    data = extract_all_tables()


    processed_data = {}


    for table_name, df in data.items():

        logger.info(
            f"Processing table: {table_name}"
        )


        # 1. Column validation
        validate_columns(
            table_name,
            df
        )


        # 2. Empty validation
        validate_not_empty(
            table_name,
            df
        )


        # 3. Duplicate validation
        primary_key = PRIMARY_KEYS[table_name]

        validate_duplicates(
            table_name,
            df,
            primary_key
        )


        # 4. NULL primary key validation
        validate_null_primary_key(
            table_name,
            df,
            primary_key
        )


        # 5. Transformation
        df = transform_data(
            table_name,
            df
        )


        processed_data[table_name] = df


    logger.info("=" * 60)
    logger.info("VALIDATION AND TRANSFORMATION COMPLETED")
    logger.info("=" * 60)


    return processed_data


if __name__ == "__main__":

    data = process_all_tables()


    print("\nProcessed Data Summary")
    print("=" * 50)


    for table_name, df in data.items():

        print(
            f"{table_name:<25} {len(df):>6} rows"
        )