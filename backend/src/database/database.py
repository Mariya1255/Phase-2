from sqlmodel import create_engine, Session
from typing import Generator
from dotenv import load_dotenv
import os

# Load environment variables from backend directory
# Try multiple locations to ensure .env is loaded
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(backend_dir, '.env')

if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # Fallback to current working directory
    load_dotenv()

# Database URL - using Neon PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create engine with proper connection parameters for Neon PostgreSQL
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session