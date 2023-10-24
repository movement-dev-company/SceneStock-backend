from random import randint


def create_confirmation_code() -> str:
    """The make_token method generates a six-digit confirmation
    code and returns it.
    """
    return str(randint(1000000, 9999999))[1::]
