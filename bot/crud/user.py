import logging

from schemas.user import User


async def register(db, user: User) -> None:
    try:
        logging.info(user)
        await db.execute(
            f"INSERT INTO Clients (id, phone, name) VALUES (?, ?, ?)",
            tuple(user.dict().values()),
        )
        await db.commit()
    except Exception as err:
        logging.error(err)
        raise err


async def get_user(db, user_id):
    user = await db.execute(f"SELECT * from Clients WHERE id = {user_id}")
    result = await user.fetchone()
    if result:
        return dict(result)
    return None
