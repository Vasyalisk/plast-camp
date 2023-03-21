from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "country_id" INT;
        ALTER TABLE "user" ADD CONSTRAINT "fk_user_country_3c9b2b9d" FOREIGN KEY ("country_id") REFERENCES "country" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP CONSTRAINT "fk_user_country_3c9b2b9d";
        ALTER TABLE "user" DROP COLUMN "country_id";"""
