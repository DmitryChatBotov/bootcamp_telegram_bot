import logging

from crm_mock.db import Database
from crm_mock.schemas.user import User


async def register(db: Database, user: User) -> None:
    """Register new user in database.
    Args:
        db: Database connection.
        user: User's info.
    """
    try:
        await db.execute(
            f"INSERT INTO Clients (id, phone, name) VALUES (?, ?, ?)",
            tuple(user.dict().values()),
        )
        await db.commit()
    except Exception as err:
        logging.error(err)
        raise err


async def get(db: Database, user_id: int) -> User:
    """Get an existing user from the database.
    Args:
        db: Database connection.
        user_id: User's ID.

    Returns:
        Info about user.
    """
    user = await db.execute(f"SELECT * from Clients WHERE id = {user_id}")
    result = await user.fetchone()
    if result:
        return User(**dict(result))
    return None
