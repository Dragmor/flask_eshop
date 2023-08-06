import sqlite3
import asyncio
import aiosqlite

async def create_table():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                price TEXT,
                image_link TEXT,
                link TEXT,
                site_group INTEGER
            )
        """)
        await db.commit()




async def write_items_to_database(items):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("DROP TABLE IF EXISTS cards")
        await db.execute("""
            CREATE TABLE cards (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                price TEXT,
                image_link TEXT,
                link TEXT,
                site_group INTEGER
            )
        """)
        for item in items:
            if "туя" in item['title'].lower():
                group = 1
            elif "можжевельник" in item['title'].lower():
                group = 2
            else:
                group = 3

            await db.execute("INSERT INTO cards (title, description, price, image_link, link, site_group) VALUES (?, ?, ?, ?, ?, ?)",
                             (item['title'], item['description'], item['price'], item['photo_link'], item['link'], group))
        await db.commit()


async def get_cards(site_group):
    # получаем карточки товаров для группы (1, 2 или 3)
    async with aiosqlite.connect("database.db") as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM cards WHERE site_group=(?)", (site_group,))
        cards = await cursor.fetchall()
        return [dict(card) for card in cards]


async def main():
    await create_table()
    
# при старте проверяем, есть-ли таблица
asyncio.run(main())