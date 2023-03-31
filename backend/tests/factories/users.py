from datetime import date

import factory

import models
from tests.factories.base import TortoiseModelFactory
from tests.factories.shared import CountryFactory


class UserFactory(TortoiseModelFactory):
    email = factory.Faker("email")
    is_email_verified = True
    password = factory.Faker("word")

    first_name = factory.Faker("word")
    last_name = factory.Faker("word")
    nickname = factory.Faker("word")
    date_of_birth = date.today()

    role = factory.Faker("random_element", elements=models.User.Role)
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.User


class BaseUserFactory(UserFactory):
    role = models.User.Role.BASE


class AdminUserFactory(UserFactory):
    role = models.User.Role.ADMIN


class SuperAdminUserFactory(UserFactory):
    role = models.User.Role.SUPER_ADMIN
