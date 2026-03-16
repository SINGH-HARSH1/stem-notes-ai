from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "sqlite+aiosqlite:///./stem_notes.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    """Base class for all the models to inherit from."""
    pass


async def get_db():
    """Dependency for providing a database session to routes"""
    async with async_session() as session:
        yield session
