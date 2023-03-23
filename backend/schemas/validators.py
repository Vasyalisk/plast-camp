from conf import settings


def validate_password(password: str):
    assert len(password) >= settings().PASSWORD_MIN_LENGTH

    has_alpha = any(one.isalpha() for one in password)
    assert has_alpha

    has_digit = any(one.isdigit() for one in password)
    assert has_digit

    has_special = any(not one.isalnum() for one in password)
    assert has_special

    return password
