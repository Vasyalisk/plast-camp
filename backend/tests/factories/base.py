import asyncio

import nest_asyncio
from factory import base

nest_asyncio.apply()

class TortoiseModelFactory(base.Factory):
    """Base factory for tortoise factory."""

    class Meta:
        abstract = True

    @classmethod
    def _create(
            cls,
            model_class,
            *args,
            **kwargs,
    ):
        """
        Creates an instance of Tortoise model.

        :param model_class: model class.
        :param args: factory args.
        :param kwargs: factory keyword-args.
        :return: instance of model class.
        """
        instance = model_class(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(instance.save())
        return instance
