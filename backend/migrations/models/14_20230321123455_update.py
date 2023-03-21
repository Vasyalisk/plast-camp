from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_email_verified" BOOL NOT NULL  DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_email_verified";"""
