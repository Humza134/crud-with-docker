from sqlmodel import Session, create_engine, SQLModel
from app.database.db_config import DB_URL

connection_string = str(DB_URL).replace(
    "postgresql", "postgresql+psycopg2"
)

engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

# Dependency with retry mechanism for OperationalError

def get_db():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    # print("Database and tables created successfully")