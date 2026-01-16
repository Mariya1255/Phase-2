from sqlmodel import create_engine, Session
from typing import Generator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database URL - using Neon PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session