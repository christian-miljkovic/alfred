import pytest
import asyncio
import nest_asyncio
from alfred.db.database import get_database
from alfred.db.db_utils import connect_to_postgres, close_postgres_connection

nest_asyncio.apply()


@pytest.fixture(scope="session")
def async_run(event_loop):
    return event_loop.run_until_complete


@pytest.fixture(scope="session")
def conn(async_run):
    async_run(connect_to_postgres())
    db = async_run(get_database())
    conn = async_run(db.pool.acquire())
    async_run(conn.execute("TRUNCATE email_details"))
    yield conn
    async_run(conn.close())
    async_run(close_postgres_connection())
