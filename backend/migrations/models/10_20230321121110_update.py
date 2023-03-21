from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "camp" ALTER COLUMN "country_id" TYPE INT USING "country_id"::INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "camp" ALTER COLUMN "country_id" TYPE INT USING "country_id"::INT;"""
