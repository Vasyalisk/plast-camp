from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "last_name" SET NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "nickname" SET NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "first_name" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "last_name" DROP NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "nickname" DROP NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "first_name" DROP NOT NULL;"""
