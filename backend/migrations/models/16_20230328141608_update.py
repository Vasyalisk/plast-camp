from typing import List

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> List[str]:
    return [
        """ALTER TABLE "camp" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ""",
        """ALTER TABLE "campmember" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ""",
        """ALTER TABLE "country" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ""",
        """ALTER TABLE "user" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ""",
        """ALTER TABLE "user" ALTER COLUMN "is_email_verified" TYPE BOOL USING "is_email_verified"::BOOL""",
        """CREATE UNIQUE INDEX "uid_campmember_camp_id_b7a1ff" ON "campmember" ("camp_id", "user_id")"""
    ]


async def downgrade(db: BaseDBAsyncClient) -> List[str]:
    return [
        """DROP INDEX "uid_campmember_camp_id_b7a1ff\"""",
        """ALTER TABLE "camp" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ""",
        """ALTER TABLE "user" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ""",
        """ALTER TABLE "user" ALTER COLUMN "is_email_verified" TYPE BOOL USING "is_email_verified"::BOOL""",
        """ALTER TABLE "country" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ""",
        """ALTER TABLE "campmember" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ"""
    ]
