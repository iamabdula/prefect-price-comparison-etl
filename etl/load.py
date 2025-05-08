# etl/load.py

from sqlalchemy.dialects.postgresql import insert as pg_insert
from utils.db_utils import get_db_engine, get_or_create_table

def load_operations_to_db(operations):
    if not operations:
        print("No operations to load.")
        return

    engine = get_db_engine()
    table = get_or_create_table(engine)

    stmt = pg_insert(table).values(operations)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_={
            "operation": stmt.excluded.operation,
            "product_details": stmt.excluded.product_details
        }
    )

    with engine.begin() as conn:
        conn.execute(stmt)
