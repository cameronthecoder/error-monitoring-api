from databases import Database

async def create_database(db_uri: str) -> Database:
    database = Database(db_uri)
    await database.connect()
    return database
