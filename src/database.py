from sqlalchemy import create_engine
from urllib.parse import quote_plus

from config.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


password = quote_plus(str(DB_PASSWORD or ""))

engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("SQLAlchemy connection successful!")