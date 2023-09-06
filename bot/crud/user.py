import logging

from schemas.user import User


async def register_user(db, user: User) -> None:
    try:
        result = await db.execute(
            "INSERT INTO Clients (id, name, phone) VALUES (?, ?, ?)",
            tuple(user.dict().values()),
        )
        logging.info(result)
    except Exception as err:
        logging.error(err)
        raise err


async def get_user(db, user_id) -> bool:
    user = await db.execute(f"SELECT * from Clients WHERE id = {user_id}")
    logging.info(user)
    if user:
        return True
    return False
