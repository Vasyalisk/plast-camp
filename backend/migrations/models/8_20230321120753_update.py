from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "camp" ALTER COLUMN "location" TYPE VARCHAR(255) USING "location"::VARCHAR(255);
        ALTER TABLE "camp" ALTER COLUMN "date_end" TYPE DATE USING "date_end"::DATE;
        ALTER TABLE "camp" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;
        ALTER TABLE "camp" ALTER COLUMN "description" TYPE VARCHAR(1024) USING "description"::VARCHAR(1024);
        ALTER TABLE "camp" ALTER COLUMN "date_start" TYPE DATE USING "date_start"::DATE;
        ALTER TABLE "camp" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
        ALTER TABLE "campmember" ALTER COLUMN "role" TYPE VARCHAR(64) USING "role"::VARCHAR(64);
        ALTER TABLE "campmember" ALTER COLUMN "user_id" TYPE INT USING "user_id"::INT;
        ALTER TABLE "campmember" ALTER COLUMN "camp_id" TYPE INT USING "camp_id"::INT;
        ALTER TABLE "campmember" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;
        ALTER TABLE "country" ALTER COLUMN "name_ukr" TYPE VARCHAR(255) USING "name_ukr"::VARCHAR(255);
        ALTER TABLE "country" ALTER COLUMN "name_orig" TYPE VARCHAR(255) USING "name_orig"::VARCHAR(255);
        ALTER TABLE "country" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "nickname" TYPE VARCHAR(127) USING "nickname"::VARCHAR(127);
        ALTER TABLE "user" ALTER COLUMN "first_name" TYPE VARCHAR(127) USING "first_name"::VARCHAR(127);
        ALTER TABLE "user" ALTER COLUMN "email" TYPE VARCHAR(320) USING "email"::VARCHAR(320);
        ALTER TABLE "user" ALTER COLUMN "last_name" TYPE VARCHAR(127) USING "last_name"::VARCHAR(127);
        ALTER TABLE "user" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "date_of_birth" TYPE DATE USING "date_of_birth"::DATE;
        ALTER TABLE "user" ALTER COLUMN "country_id" TYPE INT USING "country_id"::INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "camp" ALTER COLUMN "location" TYPE VARCHAR(255) USING "location"::VARCHAR(255);
        ALTER TABLE "camp" ALTER COLUMN "date_end" TYPE DATE USING "date_end"::DATE;
        ALTER TABLE "camp" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;
        ALTER TABLE "camp" ALTER COLUMN "description" TYPE VARCHAR(1024) USING "description"::VARCHAR(1024);
        ALTER TABLE "camp" ALTER COLUMN "date_start" TYPE DATE USING "date_start"::DATE;
        ALTER TABLE "camp" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
        ALTER TABLE "user" ALTER COLUMN "nickname" TYPE VARCHAR(127) USING "nickname"::VARCHAR(127);
        ALTER TABLE "user" ALTER COLUMN "first_name" TYPE VARCHAR(127) USING "first_name"::VARCHAR(127);
        ALTER TABLE "user" ALTER COLUMN "email" TYPE VARCHAR(320) USING "email"::VARCHAR(320);
        ALTER TABLE "user" ALTER COLUMN "last_name" TYPE VARCHAR(127) USING "last_name"::VARCHAR(127);
        ALTER TABLE "user" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "date_of_birth" TYPE DATE USING "date_of_birth"::DATE;
        ALTER TABLE "user" ALTER COLUMN "country_id" TYPE INT USING "country_id"::INT;
        ALTER TABLE "country" ALTER COLUMN "name_ukr" TYPE VARCHAR(255) USING "name_ukr"::VARCHAR(255);
        ALTER TABLE "country" ALTER COLUMN "name_orig" TYPE VARCHAR(255) USING "name_orig"::VARCHAR(255);
        ALTER TABLE "country" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;
        ALTER TABLE "campmember" ALTER COLUMN "role" TYPE VARCHAR(64) USING "role"::VARCHAR(64);
        ALTER TABLE "campmember" ALTER COLUMN "user_id" TYPE INT USING "user_id"::INT;
        ALTER TABLE "campmember" ALTER COLUMN "camp_id" TYPE INT USING "camp_id"::INT;
        ALTER TABLE "campmember" ALTER COLUMN "created_at" TYPE TIMESTAMPTZ USING "created_at"::TIMESTAMPTZ;"""
