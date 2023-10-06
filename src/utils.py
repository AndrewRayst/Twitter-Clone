import hashlib


def get_hash(input_value: str) -> str:
    return hashlib.sha256(input_value.encode()).hexdigest()
