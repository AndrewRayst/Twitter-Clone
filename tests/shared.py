from src.tweets.models import TweetModel
from src.users.models import UserModel
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

    def get_instance(self) -> UserModel:
        return UserModel(
            name=self.name,
            api_key_hash=self.api_key_hash,
        )


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
