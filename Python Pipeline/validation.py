from logger_config import logger


EXPECTED_COLUMNS = {

    "categories": [
        "category_id",
        "category_name",
        "description"
    ],

    "customers": [
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "registration_date",
        "loyalty_tier"
    ],

    "products": [
        "product_id",
        "product_name",
        "category_id",
        "unit_price",
        "cost_price",
        "stock_quantity",
        "is_active"
    ],

    "sales_transactions": [
        "transaction_id",
        "customer_id",
        "store_id",
        "transaction_date",
        "transaction_time",
        "payment_method",
        "total_amount",
        "discount_amount",
        "tax_amount",
        "net_amount"
    ],

    "sales_items": [
        "item_id",
        "transaction_id",
        "product_id",
        "quantity",
        "unit_price",
        "line_total"
    ],

    "vouchers": [
        "voucher_id",
        "voucher_code",
        "voucher_type",
        "discount_value",
        "min_purchase_amount",
        "max_discount_amount",
        "valid_from",
        "valid_to",
        "is_active"
    ],

    "voucher_redemptions": [
        "redemption_id",
        "voucher_id",
        "transaction_id",
        "customer_id",
        "redemption_date",
        "discount_applied"
    ],

    "returns": [
        "return_id",
        "transaction_id",
        "item_id",
        "customer_id",
        "product_id",
        "return_date",
        "return_quantity",
        "return_reason",
        "refund_amount",
        "refund_status"
    ]
}


def validate_columns(table_name, df):

    expected = EXPECTED_COLUMNS[table_name]

    actual = list(df.columns)

    if actual != expected:

        raise ValueError(
            f"Column mismatch for {table_name}. "
            f"Expected {expected}, got {actual}"
        )

    logger.info(
        f"Column validation passed: {table_name}"
    )


def validate_not_empty(table_name, df):

    if df.empty:

        raise ValueError(
            f"{table_name} contains zero rows"
        )

    logger.info(
        f"Row validation passed: {table_name} "
        f"({len(df)} rows)"
    )


def validate_duplicates(table_name, df, primary_key):

    duplicate_count = df[primary_key].duplicated().sum()

    if duplicate_count > 0:

        raise ValueError(
            f"{table_name} contains "
            f"{duplicate_count} duplicate {primary_key} values"
        )

    logger.info(
        f"Duplicate validation passed: {table_name}"
    )


def validate_null_primary_key(
    table_name,
    df,
    primary_key
):

    null_count = df[primary_key].isnull().sum()

    if null_count > 0:

        raise ValueError(
            f"{table_name} contains "
            f"{null_count} NULL {primary_key} values"
        )

    logger.info(
        f"NULL primary-key validation passed: {table_name}"
    )