import pandas as pd
from sqlalchemy import create_engine
import os


def excel_to_sqlite(excel_file, db_path="data.db"):
    """Convert uploaded Excel into SQLite DB (one table per sheet)."""

    if os.path.exists(db_path):
        os.remove(db_path)

    engine = create_engine(f"sqlite:///{db_path}")

    xls = pd.ExcelFile(excel_file)

    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        table_name = sheet.replace(" ", "_")
        df.to_sql(table_name, engine, index=False, if_exists="replace")

    return db_path
