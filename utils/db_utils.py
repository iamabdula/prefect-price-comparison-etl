# utils/db_utils.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql://admin:admin@etl_postgres:5432/product_ops"

def get_db_engine():
    """Creates and returns a SQLAlchemy engine."""
    eng = create_engine(DATABASE_URL)
    with eng.connect() as connection:
        print('hi')
    return eng


def get_or_create_table(engine):
    """Defines and creates the table if it doesn't exist."""
    metadata = MetaData()
    operations_table = Table(
        "product_operations", metadata,
        Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        Column("operation", String, nullable=False),
        Column("product_details", JSON, nullable=False)
    )
    metadata.create_all(engine)
    return operations_table
