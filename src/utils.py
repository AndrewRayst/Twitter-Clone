import hashlib
import random
import string


def get_hash(input_value: str) -> str:
    return hashlib.sha256(input_value.encode()).hexdigest()


def get_random_string(length: int = 10) -> str:
    if length <= 0:
        raise ValueError("length must be grater then 0")

    return "".join(random.choices(population=string.ascii_letters, k=length))
