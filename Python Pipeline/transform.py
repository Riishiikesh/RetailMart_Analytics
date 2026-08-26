import pandas as pd

from logger_config import logger


def transform_data(table_name, df):

    df = df.copy()

    # Remove leading/trailing whitespace
    string_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for column in string_columns:

        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )


    # Date transformations
    date_columns = [
        column
        for column in df.columns
        if "date" in column
        or column in ["valid_from", "valid_to"]
    ]

    for column in date_columns:

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )


    # Boolean transformation
    boolean_columns = [
        column
        for column in ["is_active"]
        if column in df.columns
    ]

    for column in boolean_columns:

        df[column] = df[column].astype("boolean")


    logger.info(
        f"Transformation completed: {table_name}"
    )

    return df