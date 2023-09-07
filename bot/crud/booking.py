"""Имитация работы CRM у заказчика с некоторыми допущениями по процедурам записи и отмены на процедуры."""
import logging
from datetime import datetime, timedelta


async def booking(
    db, client_name, service_name, booking_time, booking_date, master_name=None
):
    try:
        logging.info(f"SELECT id from Clients WHERE name = '{client_name}'")
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
        logging.info(master)
        service_result = await (
            await db.execute(
                f"SELECT id, duration, price from Services WHERE name = '{service_name}'"
            )
        ).fetchone()
        service = dict(service_result)
        logging.info(service)
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
        return {
            "master_name": master.get("name"),
            "service_name": service_name,
            "date": booking_date,
            "time": booking_time,
            "price": service.get("price"),
            'duration': service.get('duration')
        }
    except Exception as err:
        await db.rollback()
        logging.error(err)
        return False


async def cancel_booking(db, client_id: int):
    try:
        await db.execute(f"DELETE FROM Bookings WHERE client_id = {client_id}")
        await db.commit()
        return True
    except Exception as err:
        logging.info(err)
        return False
