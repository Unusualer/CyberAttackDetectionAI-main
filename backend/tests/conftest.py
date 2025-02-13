import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import Generator, AsyncGenerator
from ..app.core.config import settings
from ..app.db.base import Base
from ..app.main import app
from ..app.api.deps import get_db
from ..app.services.ml.anomaly_detection import AnomalyDetector
from ..app.services.threat_analysis import ThreatAnalysisService

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test_db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def test_db(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    TestingSessionLocal = sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
def client(test_db) -> Generator:
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_anomaly_detector():
    return AnomalyDetector()

@pytest.fixture
def test_threat_analyzer(test_anomaly_detector):
    return ThreatAnalysisService() 