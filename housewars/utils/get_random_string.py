import random
import string


def get_random_string(length: int) -> str:
    """Generates a random string of length n

    :param length int: The desired length of the returned string
    :return: A random string of length n
    """

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
