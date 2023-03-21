import factory
from datetime import date
from factory_boy_extra.tortoise_factory import TortoiseModelFactory

import models


class CountryFactory(TortoiseModelFactory):
    name_ukr = factory.Faker("word")
    name_orig = factory.Faker("word")

    class Meta:
        model = models.Country


class BaseUserFactory(TortoiseModelFactory):
    email = factory.Faker("email")
    is_email_verified = True
    password = factory.Faker("word")

    first_name = factory.Faker("word")
    last_name = factory.Faker("word")
    nickname = factory.Faker("word")
    date_of_birth = date.today()

    role = models.User.Role.BASE
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.User
