from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "campmember" ADD "user_id" INT NOT NULL;
        ALTER TABLE "campmember" ADD "camp_id" INT NOT NULL;
        ALTER TABLE "campmember" ADD CONSTRAINT "fk_campmemb_user_9f4a61a2" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;
        ALTER TABLE "campmember" ADD CONSTRAINT "fk_campmemb_camp_be9fb78d" FOREIGN KEY ("camp_id") REFERENCES "camp" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "campmember" DROP CONSTRAINT "fk_campmemb_camp_be9fb78d";
        ALTER TABLE "campmember" DROP CONSTRAINT "fk_campmemb_user_9f4a61a2";
        ALTER TABLE "campmember" DROP COLUMN "user_id";
        ALTER TABLE "campmember" DROP COLUMN "camp_id";"""
