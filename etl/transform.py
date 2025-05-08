import pandas as pd
import numpy as np

def compare_and_create_operations(before_df: pd.DataFrame, after_df: pd.DataFrame) -> list:
    """Driver function to return a unified list of all operations."""
    before_ids = set(before_df['id'])
    after_ids = set(after_df['id'])

    operations = []
    operations.extend(get_create_operations(after_df, before_ids))
    operations.extend(get_delete_operations(before_df, after_ids))
    operations.extend(get_update_operations(before_df, after_df))

    return operations

def sanitize_product_details(product_details: dict) -> dict:
    """
    Sanitize product details to ensure no invalid NaN or None values in the JSON.
    Converts NaN values to None.
    """
    for key, value in product_details.items():
        if isinstance(value, float) and (np.isnan(value) or value is None):
            product_details[key] = None  # Replace NaN or None with actual None value

    return product_details

def get_create_operations(after_df: pd.DataFrame, before_ids: set) -> list:
    """Generates create operations."""
    create_operations = []
    for _, row in after_df.iterrows():
        if row['id'] not in before_ids:
            operation = {
                "operation": "create",
                "product_details": sanitize_product_details(row.to_dict())
            }
            create_operations.append(operation)
    return create_operations

def get_delete_operations(before_df: pd.DataFrame, after_ids: set) -> list:
    """Generates delete operations."""
    delete_operations = []
    for _, row in before_df.iterrows():
        if row['id'] not in after_ids:
            operation = {
                "operation": "delete",
                "product_details": sanitize_product_details(row.to_dict())
            }
            delete_operations.append(operation)
    return delete_operations

def get_update_operations(before_df: pd.DataFrame, after_df: pd.DataFrame) -> list:
    """Generates update operations."""
    update_operations = []
    for _, after_row in after_df.iterrows():
        before_row = before_df[before_df['id'] == after_row['id']]
        if not before_row.empty and not after_row.equals(before_row.iloc[0]):
            operation = {
                "operation": "update",
                "product_details": sanitize_product_details(after_row.to_dict())
            }
            update_operations.append(operation)
    return update_operations
