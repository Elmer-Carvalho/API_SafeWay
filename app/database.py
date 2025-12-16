from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # Verifica conexões antes de usar
    pool_size=10,            # Aumenta pool para múltiplas requisições
    max_overflow=20,         # Permite picos de acesso
    pool_recycle=3600        # Recicla conexões antigas
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
