from datetime import date

import factory

import models
from tests.factories.base import TortoiseModelFactory
from tests.factories.shared import CountryFactory
from tests.factories.users import UserFactory


class CampFactory(TortoiseModelFactory):
    date_start = date.today()
    date_end = date_start.today()
    description = factory.Faker("sentence")
    location = factory.Faker("word")
    name = factory.Faker("word")
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.Camp


class CampMemberFactory(TortoiseModelFactory):
    role = factory.Faker("random_element", elements=models.CampMember.Role)
    camp = factory.SubFactory(CampFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.CampMember
