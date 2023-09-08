""""""

from os import getenv

import aiosqlite


async def create_database():
    # Подключение к базе данных
    conn = await aiosqlite.connect(getenv("SQLITE_FILE"))
    cursor = await conn.cursor()

    # Создание таблицы Masters
    await cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Masters (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL,
            start_working_hour TEXT NOT NULL,
            end_working_hour TEXT NOT NULL,
            description TEXT
        );
    """
    )

    # Создание таблицы Services
    await cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            duration INTEGER NOT NULL,
            description TEXT
        );
    """
    )

    # Создание таблицы Clients
    await cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Clients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT UNIQUE
        );
    """
    )

    # Создание таблицы Bookings
    await cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            master_id INTEGER,
            service_id INTEGER,
            date DATE NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(client_id) REFERENCES Clients(id),
            FOREIGN KEY(master_id) REFERENCES Masters(id),
            FOREIGN KEY(service_id) REFERENCES Services(id)
        );
    """
    )

    # Сохранение изменений и закрытие соединения с базой данных
    await conn.commit()
    await cursor.close()
    await conn.close()


async def insert_masters(connection):
    masters = [
        ("Alice Johnson", "09:00", "17:00", "Expert in hair styling and coloring"),
        ("Bob Smith", "10:00", "18:00", "Specializes in skin care and facials"),
        ("Charlie Brown", "11:00", "19:00", "Nail care specialist and pedicurist"),
    ]
    await connection.executemany(
        """
        INSERT INTO Masters (name, start_working_hour, end_working_hour, description)
        VALUES (?, ?, ?, ?)
        """,
        masters,
    )
    await connection.commit()


async def insert_services(connection):
    services = [
        ("Haircut & Styling", 50, 60, "Includes a wash, cut, and blow-dry"),
        ("Basic Facial", 40, 45, "A simple cleansing and moisturizing facial"),
        ("Manicure", 20, 30, "Nail shaping, cuticle cleanup, and polish"),
        ("Pedicure", 30, 45, "Foot soak, nail care, and polish"),
        ("Hair Coloring", 80, 120, "Full hair dye or highlights"),
        ("Eyebrow Threading", 15, 15, "Shaping eyebrows using a thread"),
        ("Deep Tissue Massage", 70, 90, "Massage to relieve muscle tension"),
    ]
    await connection.executemany(
        """
        INSERT INTO Services (name, price, duration, description)
        VALUES (?, ?, ?, ?)
        """,
        services,
    )
    await connection.commit()


async def insert_clients(connection):
    clients = [
        ("James Williams", "555-1234"),
        ("Jennifer Wilson", "555-1235"),
        ("Michael Jones", "555-1236"),
        ("Elizabeth Davis", "555-1237"),
        ("William Anderson", "555-1238"),
    ]
    await connection.executemany(
        """
        INSERT INTO Clients (name, phone)
        VALUES (?, ?)
        """,
        clients,
    )
    await connection.commit()


async def insert_bookings(connection):
    bookings = [
        (1, 1, 1, "2023-09-06", "09:00", "10:00", 50),
        (2, 2, 2, "2023-09-06", "10:15", "11:00", 40),
        (3, 3, 3, "2023-09-06", "11:30", "12:00", 20),
        (4, 1, 4, "2023-09-06", "12:30", "13:15", 30),
        (5, 2, 5, "2023-09-06", "13:30", "15:30", 80),
        (1, 3, 6, "2023-09-06", "16:00", "16:15", 15),
        (2, 1, 7, "2023-09-06", "10:30", "12:00", 70),
        (3, 2, 1, "2023-09-07", "10:00", "11:00", 50),
        (4, 3, 2, "2023-09-07", "11:15", "12:00", 40),
        (5, 1, 3, "2023-09-07", "12:30", "13:00", 20),
        (1, 2, 4, "2023-09-07", "13:30", "14:15", 30),
        (2, 3, 5, "2023-09-07", "14:30", "16:30", 80),
        (3, 1, 6, "2023-09-07", "16:45", "17:00", 15),
        (4, 2, 7, "2023-09-07", "11:00", "12:30", 70),
        (5, 3, 1, "2023-09-07", "13:00", "14:00", 50),
    ]
    await connection.executemany(
        """INSERT INTO Bookings (client_id, master_id, service_id, date, start_time, end_time, price) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        bookings,
    )
    await connection.commit()


async def fill_db_with_temp_data():
    conn = await aiosqlite.connect(getenv("SQLITE_FILE"))
    await insert_masters(conn)
    await insert_services(conn)
    await insert_clients(conn)
    await insert_bookings(conn)
