import os
from dotenv import load_dotenv # type: ignore
from sqlalchemy import create_engine # type: ignore

load_dotenv()

db_url = os.getenv("DB_URL")

engine = create_engine(
    db_url
)


