from databases import Database
from src.models.issues import StatusEnum
import json


async def create_database(db_url: str) -> Database:
    database = Database(db_url)
    await database.connect()
    async with database.connection() as connection:
        await connection.raw_connection._con.set_type_codec(
            "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
        )
        await connection.raw_connection._con.set_type_codec(
            "status",
            encoder=lambda type_: type_.value,
            decoder=StatusEnum,
            schema="public",
            format="text",
        )
    return database
