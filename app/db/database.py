from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, 
    pool_size=10,  
    max_overflow=20,  
    echo=False,  
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão do banco de dados.
    Use com Depends(get_db) nos endpoints do FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
