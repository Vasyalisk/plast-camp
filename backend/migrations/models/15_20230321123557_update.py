from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "is_email_verified" TYPE BOOL USING "is_email_verified"::BOOL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "is_email_verified" TYPE BOOL USING "is_email_verified"::BOOL;"""
