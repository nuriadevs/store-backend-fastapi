from app.core.settings import get_settings 
from sqlalchemy.orm import sessionmaker, declarative_base  
from sqlalchemy import create_engine  
from typing import Generator




settings = get_settings()


engine = create_engine(
    settings.DATABASE_URI,  
    pool_pre_ping=True,  
    pool_recycle=3600,  
    max_overflow=0  
)


SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False,  
    autoflush=False  
)


Base = declarative_base()

"""
Esta función proporciona una sesión de base de datos usando SessionLocal(). 
"""
def get_session() -> Generator:

    session = SessionLocal()  
    try:
        yield session  
    except Exception as e:
        session.rollback()  
        raise e  
    finally:
        session.close()  

