from databases import Database

async def create_database(db_uri: Database):
    database = Database(db_uri)
    await database.connect()
    return database
