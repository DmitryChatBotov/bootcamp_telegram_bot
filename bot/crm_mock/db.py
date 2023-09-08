from os import getenv

import aiosqlite


class Database:
    """A class for managing asynchronous connections to the database."""

    def __init__(self, db):
        self.db = db

    async def __aenter__(self):
        self.connection = await aiosqlite.connect(self.db)
        self.connection.row_factory = aiosqlite.Row
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()


async def get_db():
    """Return a database connection for use as a dependency.
    This connection has the Row factory automatically attached."""
    async with Database(getenv("SQLITE_FILE")) as db:
        yield db
