from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from app.config import settings
from app.logger import logger
from database.models import Base

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=QueuePool if settings.ENVIRONMENT == "production" else NullPool,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={"timeout": 30},
)

# Create async session factory
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize database tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


async def get_session() -> AsyncSession:
    """Get database session"""
    async with async_session() as session:
        yield session


async def close_db():
    """Close database connection"""
    await engine.dispose()


class Database:
    """Database helper class"""

    def __init__(self):
        self.engine = engine
        self.async_session = async_session

    async def execute_query(self, query):
        """Execute a query"""
        async with self.async_session() as session:
            result = await session.execute(query)
            return result

    async def add_record(self, record):
        """Add a record"""
        async with self.async_session() as session:
            session.add(record)
            await session.commit()
            return record

    async def update_record(self, record):
        """Update a record"""
        async with self.async_session() as session:
            merged = await session.merge(record)
            await session.commit()
            return merged

    async def delete_record(self, record):
        """Delete a record"""
        async with self.async_session() as session:
            await session.delete(record)
            await session.commit()


db = Database()