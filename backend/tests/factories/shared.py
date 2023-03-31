import factory

import models
from tests.factories.base import TortoiseModelFactory


class CountryFactory(TortoiseModelFactory):
    name_ukr = factory.Faker("word")
    name_orig = factory.Faker("word")

    class Meta:
        model = models.Country
