from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "camp" ADD "country_id" INT;
        ALTER TABLE "camp" ADD CONSTRAINT "fk_camp_country_993d9af0" FOREIGN KEY ("country_id") REFERENCES "country" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "camp" DROP CONSTRAINT "fk_camp_country_993d9af0";
        ALTER TABLE "camp" DROP COLUMN "country_id";"""
