import asyncio
import os
import typing as t

import typer
from tortoise import Tortoise

from admin import utils as admin_utils
from db import TORTOISE_CONFIG
from migrations.utils import command as migration_command

cli = typer.Typer(rich_markup_mode="rich")


def run_async(f: t.Awaitable):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(f)


@cli.command(help="Migrate [green]initial (zero)[/green] migration on a fresh DB")
def upgrade_zero_migration():
    run_async(migration_command.upgrade_zero())


@cli.command(help=(
        "Create default superadmin if [green]ADMIN_EMAIL[/green] and [green]ADMIN_PASSWORD[/green] env variables "
        "are provided"
))
def create_default_superadmin():
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not email or not password:
        typer.echo("No ADMIN_EMAIL or ADMIN_PASSWORD is set", err=True)
        return

    async def _run():
        await Tortoise.init(config=TORTOISE_CONFIG)
        await admin_utils.create_superadmin(email, password)

    run_async(_run())


@cli.command(help="Create custom superadmin if not exists")
def create_superadmin(
        email: t.Annotated[str, typer.Option(prompt=True)],
        password: t.Annotated[str, typer.Option(prompt=True)],
):
    async def _run():
        await Tortoise.init(config=TORTOISE_CONFIG)
        await admin_utils.create_superadmin(email, password)

    run_async(_run())


if __name__ == "__main__":
    cli()
