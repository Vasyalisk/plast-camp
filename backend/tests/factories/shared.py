from tests.factories.base import TortoiseModelFactory
import factory
import models


class CountryFactory(TortoiseModelFactory):
    name_ukr = factory.Faker("word")
    name_orig = factory.Faker("word")

    class Meta:
        model = models.Country
