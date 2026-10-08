# 🛒 RetailMart Analytics

**RetailMart Analytics** is an end-to-end **Retail Data Engineering and
Analytics pipeline** built to demonstrate how transactional retail data
can be extracted from **MySQL**, validated and transformed with
**Python**, loaded into **Google BigQuery**, and modeled into a **star
schema** for analytics.

The project covers the complete flow from **OLTP source data → ETL →
cloud data warehouse → dimensional modeling → analytical SQL
procedures**.

------------------------------------------------------------------------

## 📌 Problem Statement

Retail businesses generate data across customers, products, stores,
sales, vouchers, and product returns.

A transactional database is useful for day-to-day operations, but it is
not ideal for analytical workloads such as:

-   Monthly revenue analysis
-   Month-over-Month (MoM) growth
-   Year-over-Year (YoY) growth
-   Product and category performance
-   Customer analysis
-   Store-level sales analysis
-   Return rate and refund impact analysis
-   Voucher and discount analysis

This project builds a structured data pipeline that converts operational
retail data into an analytics-ready warehouse model.

------------------------------------------------------------------------

## 🎯 Project Objective

The main objective is to build a reliable and reusable data pipeline
that:

1.  Stores retail transactions in a normalized **MySQL OLTP database**.
2.  Extracts data from MySQL using **Python and Pandas**.
3.  Performs data-quality validation before loading.
4.  Applies basic transformations such as trimming strings, date
    conversion, and boolean normalization.
5.  Loads processed data into **Google BigQuery**.
6.  Creates a dimensional **star schema** for analytics.
7.  Provides reusable SQL procedures for sales and returns analysis.

------------------------------------------------------------------------

## 🏗️ End-to-End Architecture

``` text
                    ┌─────────────────────┐
                    │   RetailMart Data   │
                    │      CSV Files      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   MySQL OLTP DB     │
                    │                     │
                    │ Customers           │
                    │ Products            │
                    │ Sales               │
                    │ Vouchers            │
                    │ Returns             │
                    └──────────┬──────────┘
                               │
                         Python ETL
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
          Extract           Validate        Transform
          Pandas            PK / NULL       Dates
                            Duplicate       Strings
                            Columns         Boolean
              └────────────────┼────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   BigQuery Raw      │
                    │   retailmart_raw    │
                    └──────────┬──────────┘
                               │
                    Dimensional Modeling
                               │
                               ▼
                    ┌─────────────────────┐
                    │ BigQuery Analytics  │
                    │ retailmart_analytics│
                    │                     │
                    │ dim_customer        │
                    │ dim_date            │
                    │ dim_product        │
                    │ dim_store           │
                    │ fact_sales          │
                    │ fact_returns        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Analytical SQL      │
                    │ Procedures          │
                    │                     │
                    │ Sales Metrics       │
                    │ Returns Analysis    │
                    └─────────────────────┘
```

------------------------------------------------------------------------

## 🧩 MySQL ER Diagram

The source system is designed as a normalized retail transaction
database.

![RetailMart MySQL ER Diagram](MySQL%20ER%20Diagram.png)

The ER model contains entities for:

-   Categories
-   Customers
-   Products
-   Sales Transactions
-   Sales Items
-   Vouchers
-   Voucher Redemptions
-   Returns

------------------------------------------------------------------------

## 🗄️ Source Database --- MySQL

The MySQL database is named:

``` text
retailmart
```

### Core Tables

  -----------------------------------------------------------------------
  Table                               Purpose
  ----------------------------------- -----------------------------------
  `categories`                        Stores product category information

  `customers`                         Stores customer and loyalty
                                      information

  `products`                          Stores product, pricing, stock, and
                                      category information

  `sales_transactions`                Stores transaction-level sales
                                      information

  `sales_items`                       Stores individual products sold
                                      within transactions

  `vouchers`                          Stores voucher and discount
                                      definitions

  `voucher_redemptions`               Tracks voucher usage against
                                      transactions

  `returns`                           Stores returned products and refund
                                      information
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 📊 Sample Dataset

The project includes generated retail data covering **2023--2024**.

  Dataset                 Records
  --------------------- ---------
  Categories                   10
  Customers                    50
  Products                     50
  Sales Transactions        5,000
  Sales Items              15,047
  Vouchers                    100
  Voucher Redemptions         300
  Returns                     500

The dataset is generated programmatically using Python, making it easy
to recreate the project with a fresh dataset.

------------------------------------------------------------------------

## 🔄 ETL Pipeline

### 1. Extract

Python connects to MySQL and extracts all source tables using Pandas.

``` text
MySQL
   ↓
mysql.connector
   ↓
Pandas DataFrames
```

The extraction layer processes:

``` text
categories
customers
products
sales_transactions
sales_items
vouchers
voucher_redemptions
returns
```

------------------------------------------------------------------------

### 2. Validate

Before loading data into BigQuery, the pipeline performs multiple
data-quality checks.

#### Column Validation

Confirms that every source table contains the expected columns and
column order.

#### Empty Table Validation

Ensures that required tables contain data.

#### Duplicate Primary-Key Validation

Checks for duplicate primary-key values.

#### NULL Primary-Key Validation

Ensures primary-key columns do not contain NULL values.

Example validation flow:

``` text
Extract
   ↓
Column Validation
   ↓
Empty Data Validation
   ↓
Duplicate PK Validation
   ↓
NULL PK Validation
   ↓
Transform
```

------------------------------------------------------------------------

### 3. Transform

The Python transformation layer performs lightweight standardization:

-   Removes leading/trailing whitespace from string columns
-   Converts date-related columns into datetime format
-   Converts `is_active` fields into boolean values
-   Preserves the source table structure for warehouse loading

------------------------------------------------------------------------

### 4. Load

Validated and transformed Pandas DataFrames are loaded into **Google
BigQuery**.

The pipeline uses:

``` text
WRITE_TRUNCATE
```

for the raw tables, meaning the target table is replaced during each
full load.

A row-count validation is also performed after every BigQuery load:

``` text
Source Row Count == BigQuery Row Count
```

If the counts do not match, the pipeline raises an error.

------------------------------------------------------------------------

## ☁️ Google BigQuery Architecture

The project uses two logical BigQuery layers.

### Raw Layer

``` text
retailmart_raw
```

Contains the processed source tables loaded from MySQL.

### Analytics Layer

``` text
retailmart_analytics
```

Contains the dimensional model designed for analytical workloads.

------------------------------------------------------------------------

## ⭐ Star Schema

The analytics layer follows a **star schema** consisting of dimension
and fact tables.

### Dimension Tables

``` text
dim_customer
dim_date
dim_product
dim_store
```

### Fact Tables

``` text
fact_sales
fact_returns
```

### Fact Sales

`fact_sales` captures sales at the **sales-item level**.

Important measures include:

-   Quantity
-   Unit Price
-   Gross Revenue

Key dimensions include:

-   Date
-   Product
-   Customer
-   Store

### Fact Returns

`fact_returns` captures product return activity.

Important measures include:

-   Quantity Returned
-   Refund Amount
-   Return Rate
-   Revenue Impact

------------------------------------------------------------------------

## 📐 Analytics Data Model

``` text
                    ┌───────────────┐
                    │  dim_customer │
                    └───────┬───────┘
                            │
                            │
┌─────────────┐      ┌──────▼──────┐      ┌─────────────┐
│  dim_date   │─────▶│ fact_sales  │◀─────│ dim_product │
└─────────────┘      └──────┬──────┘      └─────────────┘
                            │
                            │
                     ┌──────▼──────┐
                     │  dim_store  │
                     └─────────────┘


                    ┌───────────────┐
                    │  dim_customer │
                    └───────┬───────┘
                            │
┌─────────────┐      ┌──────▼───────┐      ┌─────────────┐
│  dim_date   │─────▶│ fact_returns │◀─────│ dim_product │
└─────────────┘      └──────────────┘      └─────────────┘
```

------------------------------------------------------------------------

## 📈 Analytical SQL Procedures

The project includes reusable BigQuery stored procedures for business
analysis.

### 1. Sales Metrics

``` text
sp_sales_metrics
```

Accepts:

``` text
input_year
input_month
```

and calculates:

-   Current month revenue
-   Previous month revenue
-   Month-over-Month (MoM) percentage
-   Previous year same-month revenue
-   Year-over-Year (YoY) percentage

Example:

``` sql
CALL `retailmart-analytics-506321.retailmart_analytics.sp_sales_metrics`(
    2024,
    2
);
```

------------------------------------------------------------------------

### 2. Returns Analysis

``` text
sp_returns_analysis
```

Accepts:

``` text
input_year
input_month
```

and analyzes:

-   Total returns
-   Quantity returned
-   Quantity sold
-   Return rate percentage
-   Revenue/refund impact
-   Category-level return performance

Example:

``` sql
CALL `retailmart-analytics-506321.retailmart_analytics.sp_returns_analysis`(
    2023,
    3
);
```

------------------------------------------------------------------------

## 🐍 Python Technologies

  Technology              Purpose
  ----------------------- ---------------------------------------
  Python                  ETL orchestration and data processing
  Pandas                  Data extraction and transformation
  MySQL Connector         MySQL connectivity
  python-dotenv           Environment configuration
  Google Cloud BigQuery   Cloud data warehouse
  Logging                 ETL monitoring and error tracking

------------------------------------------------------------------------

## ☁️ Cloud Technologies

-   **Google BigQuery** --- Cloud data warehouse
-   **Google Cloud IAM / Service Account** --- Authentication and access
-   **BigQuery SQL** --- Analytical modeling and stored procedures

------------------------------------------------------------------------

## 📂 Project Structure

``` text
RetailMart_Analytics/
│
├── BigQuery Schema/
│   ├── Create_Star_Schema_retailmart_analytics.sql
│   ├── dim_customer.sql
│   ├── dim_date.sql
│   ├── dim_product.sql
│   ├── dim_store.sql
│   ├── fact_sales.sql
│   └── fact_returns.sql
│
├── MySQL Schema/
│   ├── 01_create_database.sql
│   └── Load_data.sql
│
├── SQL Procedures/
│   ├── sp_sales_metrics.sql
│   └── sp_returns_analysis.sql
│
├── Python Pipeline/
│   ├── config.py
│   ├── create_dataset.py
│   ├── extract_mysql.py
│   ├── load_bigquery.py
│   ├── logger_config.py
│   ├── mysql_connection.py
│   ├── process_data.py
│   ├── transform.py
│   ├── validation.py
│   ├── test_mysql.py
│   └── test_bigquery.py
│
├── data/
│   ├── categories.csv
│   ├── customers.csv
│   ├── products.csv
│   ├── sales_transactions.csv
│   ├── sales_items.csv
│   ├── vouchers.csv
│   ├── voucher_redemptions.csv
│   ├── returns.csv
│   └── generate_data.py
│
├── logs/
│   └── etl.log
│
├── MySQL ER Diagram.png
├── .env
└── README.md
```

------------------------------------------------------------------------

## ⚙️ Setup Instructions

### 1. Prerequisites

Install the following:

-   Python 3.9+
-   MySQL 8.0+
-   Google Cloud account
-   BigQuery enabled
-   Google Cloud authentication configured

------------------------------------------------------------------------

### 2. Install Python Dependencies

``` bash
pip install pandas
pip install mysql-connector-python
pip install python-dotenv
pip install google-cloud-bigquery
pip install pyarrow
```

Or:

``` bash
pip install pandas mysql-connector-python python-dotenv google-cloud-bigquery pyarrow
```

------------------------------------------------------------------------

### 3. Configure Environment Variables

Create a `.env` file:

``` env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=retailmart
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password

GCP_PROJECT_ID=your_gcp_project_id
BIGQUERY_DATASET=retailmart_raw
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

Do **not** commit `.env` or service-account credentials to GitHub.

------------------------------------------------------------------------

### 4. Generate Sample Data

If you want to regenerate the sample dataset:

``` bash
cd data
python generate_data.py
```

The generator creates sales transactions, sales items, vouchers, voucher
redemptions, and returns.

------------------------------------------------------------------------

### 5. Create MySQL Database

Run:

``` text
MySQL Schema/01_create_database.sql
```

This creates the `retailmart` database and its source tables.

Load the CSV files into the corresponding MySQL tables.

> Update the `LOAD DATA LOCAL INFILE` path in `Load_data.sql` according
> to your local machine.

------------------------------------------------------------------------

### 6. Test MySQL Connection

From the `Python Pipeline` directory:

``` bash
python test_mysql.py
```

Expected output:

``` text
Connected database: retailmart
```

------------------------------------------------------------------------

### 7. Create BigQuery Dataset

Run:

``` bash
python create_dataset.py
```

This creates the configured BigQuery dataset if it does not already
exist.

------------------------------------------------------------------------

### 8. Run the ETL Pipeline

The main processing flow is:

``` text
MySQL
  ↓
Extract
  ↓
Validate
  ↓
Transform
  ↓
Load to BigQuery
  ↓
Row Count Validation
```

Run:

``` bash
python load_bigquery.py
```

The pipeline logs:

-   Extraction status
-   Validation status
-   Transformation status
-   BigQuery loading status
-   Row-count validation
-   Errors and failures

Logs are written to:

``` text
logs/etl.log
```

------------------------------------------------------------------------

### 9. Build the Analytics Star Schema

After the raw tables are available in BigQuery, run the SQL scripts
inside:

``` text
BigQuery Schema/
```

Recommended order:

``` text
1. Create_Star_Schema_retailmart_analytics.sql
2. dim_customer.sql
3. dim_date.sql
4. dim_product.sql
5. dim_store.sql
6. fact_sales.sql
7. fact_returns.sql
```

------------------------------------------------------------------------

### 10. Create Analytical Procedures

Run:

``` text
SQL Procedures/sp_sales_metrics.sql
SQL Procedures/sp_returns_analysis.sql
```

You can then call the procedures with a year and month to generate
business metrics.

------------------------------------------------------------------------

## 🧪 Data Quality & Reliability

The ETL pipeline includes several controls to reduce bad data entering
the warehouse.

### Validation Checks

``` text
✓ Expected columns
✓ Non-empty tables
✓ Duplicate primary keys
✓ NULL primary keys
✓ Source vs target row counts
```

### ETL Logging

The pipeline uses Python's logging framework to maintain an execution
log.

Example:

``` text
2026-08-22 23:xx:xx | INFO | MySQL connection successful
2026-08-22 23:xx:xx | INFO | Column validation passed
2026-08-22 23:xx:xx | INFO | Transformation completed
2026-08-22 23:xx:xx | INFO | BigQuery load completed
```

------------------------------------------------------------------------

## 💼 Business Questions This Project Can Answer

The analytics model can support questions such as:

-   What was total revenue in a given month?
-   How did revenue change compared with the previous month?
-   How did revenue compare with the same month last year?
-   Which product categories generate the most sales?
-   Which products have the highest return volume?
-   What percentage of sold quantity was returned?
-   Which categories have the highest refund impact?
-   How do stores perform against each other?
-   Which customers and loyalty tiers generate the most business?
-   How much discount and voucher activity occurs across transactions?

------------------------------------------------------------------------

## 🚀 Future Enhancements

The current project can be extended with:

-   **Cloud Composer / Airflow** for workflow orchestration
-   **Cloud Storage** as a landing zone
-   **Incremental ETL** instead of full refresh
-   **BigQuery partitioning and clustering optimization**
-   **dbt** for warehouse transformations and testing
-   **Power BI / Looker Studio** dashboards
-   Automated data-quality monitoring
-   CI/CD for SQL and Python pipeline deployment
-   Metadata and lineage tracking
-   Slowly Changing Dimensions (SCD Type 2)
-   Alerting for ETL failures

------------------------------------------------------------------------

## 🔐 Security Note

**Never commit credentials to GitHub.**

Before publishing this project:

``` text
.env
service-account JSON
database passwords
private keys
```

should be removed from the repository and added to `.gitignore`.

If a service-account key has already been exposed publicly,
revoke/rotate it in Google Cloud before publishing the repository.

------------------------------------------------------------------------

## 🎓 Skills Demonstrated

This project demonstrates practical experience with:

-   Data Engineering
-   ETL / ELT
-   Python
-   Pandas
-   MySQL
-   SQL
-   BigQuery
-   Data Validation
-   Data Quality
-   Dimensional Modeling
-   Star Schema
-   Fact & Dimension Tables
-   Stored Procedures
-   Cloud Data Warehousing
-   Logging & Error Handling
-   Retail Analytics

------------------------------------------------------------------------

## 📌 Project Summary

**RetailMart Analytics** demonstrates a complete retail data engineering
workflow:

``` text
Raw Retail Data
      ↓
MySQL OLTP
      ↓
Python ETL
      ↓
Data Validation
      ↓
Transformation
      ↓
BigQuery Raw Layer
      ↓
Star Schema
      ↓
Sales & Returns Analytics
```

The project is designed as a practical portfolio implementation of an
**end-to-end cloud data pipeline**, combining traditional relational
databases, Python-based ETL, Google BigQuery, dimensional modeling, and
analytical SQL.

------------------------------------------------------------------------

## 👨‍💻 Author

**Rishikesh**

Data Engineering \| Python \| SQL \| BigQuery \| ETL \| Data Warehousing
