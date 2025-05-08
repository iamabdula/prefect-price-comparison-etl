import pandas as pd
from prefect import flow, task
from extract import extract_product_data
from transform import compare_and_create_operations
from load import load_operations_to_db

# Prefect task for extraction
@task
def extract_data():
    """
    Task to extract product data (before and after) from local CSV files.
    Returns:
        tuple: before_df, after_df (pandas DataFrames).
    """
    before_df, after_df = extract_product_data()
    return before_df, after_df

# Prefect task for transformation
@task
def transform_data(before_df: pd.DataFrame, after_df: pd.DataFrame):
    """
    Task to transform the data, calculating create, update, and delete operations.
    Returns:
        list: Operations to be loaded into the database.
    """
    operations = compare_and_create_operations(before_df, after_df)
    return operations

# Prefect task for loading into DB
@task
def load_data(operations: list):
    """
    Task to load operations into the PostgreSQL database.
    """
    load_operations_to_db(operations)

# Prefect flow to orchestrate ETL process
@flow
def etl_flow():
    """
    Orchestrates the ETL pipeline: extract data, transform it, and load it into the DB.
    """
    # Step 1: Extract data
    before_df, after_df = extract_data()

    # Step 2: Transform data
    operations = transform_data(before_df, after_df)

    # Step 3: Load data into the database
    load_data(operations)

    print("ETL process completed successfully!")

# To run the flow, simply call etl_flow()
if __name__ == "__main__":
    etl_flow()
