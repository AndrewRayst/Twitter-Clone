from src.tweets.models import TweetModel
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
    user: UserTestDataClass
    content: str
    id: int = 0

    def __init__(self, user: UserTestDataClass):
        self.user = user
        self.content = get_random_string()

    def get_instance(self) -> TweetModel:
        return TweetModel(
            content=self.content,
            user_id=self.user.id,
        )


TUsersTest = tuple[UserTestDataClass, UserTestDataClass, UserTestDataClass]
