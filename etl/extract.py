import pandas as pd
import os
from dotenv import load_dotenv
from io import StringIO
import boto3

# Load environment variables from the .env file
load_dotenv()

# File path for local CSV extraction (for now)
# LOCAL_PATH_BEFORE = os.getenv("LOCAL_PATH_BEFORE")
# LOCAL_PATH_AFTER = os.getenv("LOCAL_PATH_AFTER")
LOCAL_PATH_BEFORE="data/product_inventory_before.csv"
LOCAL_PATH_AFTER="data/product_inventory_after.csv"
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")  # For future use when switching to S3


def extract_local(file_path: str) -> pd.DataFrame:
    """
    Extracts data from a local CSV file and returns it as a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The DataFrame containing product data.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded data from {file_path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at: {file_path}")
    except Exception as e:
        raise Exception(f"Error occurred while loading CSV: {e}")


def extract_s3(bucket_name: str, file_key: str) -> pd.DataFrame:
    """
    Extracts data from a CSV file stored on S3 and returns it as a pandas DataFrame.

    Args:
        bucket_name (str): The S3 bucket name.
        file_key (str): The S3 file key.

    Returns:
        pd.DataFrame: The DataFrame containing product data.
    """
    try:
        # Using boto3 to get the CSV file from S3
        s3_client = boto3.client("s3")
        csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_data = csv_obj["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(csv_data))
        print(f"Successfully loaded data from S3: {file_key}")
        return df
    except Exception as e:
        raise Exception(f"Error occurred while loading CSV from S3: {e}")


def extract_product_data() -> tuple:
    """
    Extracts product data from both 'before' and 'after' CSV files.
    For local files for now, but can easily be switched to S3.

    Returns:
        tuple: Contains DataFrames for 'before' and 'after' product data.
    """
    if LOCAL_PATH_BEFORE and LOCAL_PATH_AFTER:
        before_data = extract_local(LOCAL_PATH_BEFORE)
        after_data = extract_local(LOCAL_PATH_AFTER)
    elif S3_BUCKET_NAME:  # If S3 is set in the .env file, extract from S3
        before_data = extract_s3(S3_BUCKET_NAME, "product_inventory_before.csv")
        after_data = extract_s3(S3_BUCKET_NAME, "product_inventory_after.csv")
    else:
        raise ValueError("No valid extraction source found (local or S3).")

    return before_data, after_data
