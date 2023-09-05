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
