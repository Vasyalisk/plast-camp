from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "campmember" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "role" VARCHAR(64) NOT NULL
);
COMMENT ON COLUMN "campmember"."role" IS 'STAFF: STAFF\nPARTICIPANT: PARTICIPANT\nGUEST: GUEST';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "campmember";"""
