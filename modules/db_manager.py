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