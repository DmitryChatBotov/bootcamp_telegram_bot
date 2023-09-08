"""Imitation of CRM work at the customer with some assumptions regarding the procedures for recording and canceling procedures."""
import logging
from datetime import datetime, timedelta

from crm_mock.db import Database
from crm_mock.schemas.booking import Reservation


async def create_reservation(
    db: Database,
    client_name: str,
    service_name: str,
    booking_time: str,
    booking_date: str,
    master_name: str = None,
) -> Reservation | None:
    try:
        user_result = await (
            await db.execute(f"SELECT id from Clients WHERE name = '{client_name}'")
        ).fetchone()
        client_id = dict(user_result)["id"]
        if master_name:
            master_result = await (
                await db.execute(
                    f"SELECT id, name from Masters WHERE name = '{master_name}'"
                )
            ).fetchone()
        else:
            master_result = await (
                await db.execute(f"SELECT id, name from Masters")
            ).fetchone()
        master = dict(master_result)
        service_result = await (
            await db.execute(
                f"SELECT id, duration, price from Services WHERE name = '{service_name}'"
            )
        ).fetchone()
        service = dict(service_result)
        end_time = datetime.strptime(booking_time, "%H:%M") + timedelta(
            minutes=service.get("duration", 0)
        )
        end_time = end_time.strftime("%H:%M")
        await db.execute(
            f"INSERT INTO Bookings (client_id, master_id, service_id, date, start_time, end_time, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                client_id,
                master.get("id"),
                service.get("id"),
                booking_date,
                booking_time,
                end_time,
                service.get("price"),
            ),
        )
        await db.commit()
        return Reservation(
            master=master.get("name"),
            beauty_procedure=service_name,
            date=booking_date,
            time=booking_time,
            price=service.get("price"),
            duration=service.get("duration"),
        )
    except Exception as err:
        await db.rollback()
        logging.error(err)


async def cancel_reservation(db: Database, client_id: int):
    try:
        await db.execute(f"DELETE FROM Bookings WHERE client_id = {client_id}")
        await db.commit()
    except Exception as err:
        raise err
