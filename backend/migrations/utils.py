import asyncio
import os

import aerich
import click
from aerich.enums import Color

from db import TORTOISE_CONFIG


class ZeroCommand(aerich.Command):
    async def upgrade_zero(self):
        migrations_dir = os.path.join(self.location, self.app)
        _, _, migration_names = next(os.walk(migrations_dir))

        try:
            version = next(one for one in migration_names if one.startswith("0_"))
        except StopIteration:
            click.secho(f"{migrations_dir} does not contain zero migration")
            return

        await aerich.Tortoise.init(config=self.tortoise_config)
        connection = aerich.get_app_connection(self.tortoise_config, self.app)
        await aerich.generate_schema_for_client(connection, safe=True)

        if await aerich.Aerich.exists():
            click.secho(f"Already upgraded", fg=Color.red)
            return

        await aerich.Aerich.create(
            version=version,
            app=self.app,
            content={},
        )
        click.secho(f"Success upgrade {version}", fg=Color.green)

    def upgrade_zero_sync(self):
        asyncio.run(self.upgrade_zero())


command = ZeroCommand(tortoise_config=TORTOISE_CONFIG, app="models")
