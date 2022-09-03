import random
import string


def get_random_string(length):
    """Generates a random string of length n

    Parameters
    ----------
    length : int
        The desired length of the returned string

    Returns
    -------
    str
        A random string of length n
    """

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
