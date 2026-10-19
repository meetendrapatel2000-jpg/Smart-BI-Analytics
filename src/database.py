from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = DATA_DIR / "dashboard.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}")

with engine.begin() as connection:
    csv_files = list(DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {DATA_DIR}"
        )

    for csv_file in csv_files:
        if csv_file.stem == "dashboard":
            continue

        df = pd.read_csv(csv_file)
        df.to_sql(
            csv_file.stem,
            connection,
            if_exists="replace",
            index=False
        )

print("Local CSV database loaded successfully!")