from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a password using the specified password context.

    Parameters:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify if a given password matches a hashed password.

    Parameters:
        password (str): The password to be verified.
        hashed_password (str): The hashed password to be compared.

    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """
    return pwd_context.verify(password, hashed_password)
