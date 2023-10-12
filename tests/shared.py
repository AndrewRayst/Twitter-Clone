from src.utils import get_hash, get_random_string


class UserTestDataClass:
    api_key: str
    api_key_hash: str
    name: str
    id: int = 0

    def __init__(self):
        self.name = get_random_string()
        self.api_key = get_random_string()
        self.api_key_hash = get_hash(self.api_key)

    def __dict__(self) -> dict:
        return {
            "api_key_hash": self.api_key_hash,
            "name": self.name,
        }


class TweetTestDataClass:
    user_id: id
    content: str
    id: int = 0

    def __init__(self, user_id: id):
        self.user_id = user_id
        self.content = get_random_string()

    def __dict__(self) -> dict:
        return {
            "content": self.content,
            "user_id": self.user_id,
        }


TUsersTest = tuple[UserTestDataClass, UserTestDataClass, UserTestDataClass]
