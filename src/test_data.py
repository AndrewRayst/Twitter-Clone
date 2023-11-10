from datetime import datetime

from src.database.core import session_maker
from src.media.models import MediaModel
from src.tweets.models import TweetLikeModel, TweetModel
from src.users.models import UserFollowerModel, UserModel

DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f"

USERS: list[tuple[str, str]] = [
    ("test", "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"),
    ("Tom", "7ee01a317295bbe8a3f8c7673af7c665e5cded8a5f984e2f357b77d443b5ed9d"),
    ("Mot", "1fb3ffaddb60be2ab0e2e76d0bed3d5074a3faab5bc3b34339634df97310d589"),
    ("Kim", "b7c943fa05691b0bd60824844ade9994277ccd5ab293235828ee103ce8d5d42e"),
    ("Michael", "329a3c612239f0a72c69e8e42c87c5f8cbf613dcd4889da0411b3c4f18c3bf15"),
    ("Mary", "fa212d1dd25ac1b260fe9b6ff7c37f9ca0de2fccd65a065a0b2f942f05277c8b"),
]

FOLLOWERS: list[tuple[int, int]] = [
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (3, 2),
    (4, 2),
    (5, 2),
    (2, 3),
    (4, 3),
    (5, 3),
    (6, 3),
    (6, 4),
    (5, 4),
    (2, 5),
    (6, 5),
    (4, 5),
    (4, 6),
    (5, 6),
]

MEDIA: list[tuple[str, int, int]] = [
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "GMUJKYpDhU6ea82f87-99f6-402c-a0d8-e378b7483668.png",
        1,
        2,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "ItajoEqoWG63a6e893-b7d6-49ae-8d67-4dd8f995a527.jpeg",
        2,
        3,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "ONkSmjrKDK0e945507-4028-4466-84bc-4758bb3adc59.webp",
        16,
        3,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "DzMgMaCtCOf47a786b-4792-4d82-a41e-453f17a2d43f.jpeg",
        3,
        4,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "mWCTSsSjvL26583e2a-06c1-4881-aeb2-f57dccac126a.webp",
        4,
        6,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "QdjodYZqfW849f26af-cde1-4ba7-903e-33376d698941.webp",
        5,
        5,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "zLFAqdQNxF7eed3d6f-9228-4cf1-add9-a7ce30d6353e.jpeg",
        17,
        4,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "jwwvbqXFMGa055d0bb-871c-4011-a0b1-29c5ae646cb9.jpeg",
        6,
        2,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "cRnDnZYWqo1eec6870-d39d-4de7-9e3c-016affb0a133.jpeg",
        18,
        5,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "GWzXwKsSWX27375961-e7bb-4c3c-8afc-92d5aac02637.webp",
        19,
        6,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "nBxWvNTUtD1d52cc64-f01a-49f6-b23c-dfbf7b9ad551.jpeg",
        7,
        4,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "IfoXmglele8ac03294-5fb9-46e0-ae94-4af7bdb4df09.webp",
        7,
        4,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "dDZgmoZKIV7450bfd4-50dc-43d1-bb81-9a9923b15c10.jpeg",
        7,
        4,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "CzUIpmDAUw251a0289-9ce9-4c23-998b-2677f177e456.jpeg",
        21,
        3,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "yjKiUEwGRpc36809be-dc48-48d6-81a2-93d1facd5a82.jpeg",
        8,
        5,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "eBnZxiWGGtfcc7ba27-dd73-4788-935a-46c6ac6c1be5.jpeg",
        9,
        6,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "PkJNviVYJp502cdd42-dc49-4f75-9c73-bc1d256b791a.png",
        10,
        2,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "OfmgYqflXUd64bdf39-5bb1-44f2-867f-d76c45ffb426.webp",
        11,
        3,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "hgDwlRyqUn3f846603-952d-4061-84da-5ed159d3cdac.jpeg",
        12,
        4,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "cthqxcgZyue05b9a03-a402-4bd2-8a30-e301ede45808.jpeg",
        13,
        5,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "nbJhMcgWKsf72df64b-238a-40be-8283-5c4da1ee42e5.jpeg",
        14,
        6,
    ),
    (
        "https://storage.yandexcloud.net/twitter-clone/images/"
        "hHUBXyVYQGad6b36fe-0beb-4770-9add-238370ab1610.jpeg",
        15,
        2,
    ),
]

TWEETS: list[tuple[int, str, str]] = [
    (2, "I started learning python!!!", "2023-11-06 07:23:37.275879"),
    (3, "Cool game", "2023-11-06 07:25:22.221851"),
    (
        4,
        "Look how beautiful the lake is. It was a great weekend",
        "2023-11-06 07:29:22.755674",
    ),
    (
        6,
        "Breakfast with my best friend @Kim\n#breakfast\n#cafe\n#coffee\n#bestie",
        "2023-11-06 07:32:33.020593",
    ),
    (5, "My morning routine", "2023-11-06 07:35:46.07945"),
    (2, "Ha-ha-ha-ha", "2023-11-06 07:39:38.995315"),
    (
        4,
        "Who wants some bounty? 🥥\nVacation is going great!!!",
        "2023-11-06 07:52:40.171164",
    ),
    (5, "Small snack", "2023-11-06 07:55:00.69269"),
    (
        6,
        "Lunch❤️❤️❤️\n#lunch\n#food\n#health\n#healthyfoods",
        "2023-11-06 07:58:24.436444",
    ),
    (2, "It's so hilarious😂😂", "2023-11-06 08:06:12.872974"),
    (
        3,
        "Today a new game came out for my microwave!!! "
        "I play while the food is heating up, I think this is the best game of 2035. "
        "Plays without a single bug or error. "
        "Developed by the best company in the world, led by Todd, a great guy. "
        "He has a wonderful phrase: “it just works.”",
        "2023-11-06 08:16:24.800529",
    ),
    (4, "At a business meeting😎", "2023-11-06 08:19:52.68914"),
    (5, "Training🏋", "2023-11-06 08:22:15.092433"),
    (6, "Look what dinner I prepared😍", "2023-11-06 08:29:06.427571"),
    (2, "$is_joke = True;", "2023-11-06 08:35:04.709247"),
    (
        3,
        "There are so many new mechanics, all sorts of cards...",
        "2023-11-06 08:37:15.924701",
    ),
    (4, "I have long dreamed of visiting Paris!!!", "2023-11-06 08:39:04.530471"),
    (5, "What a beautiful sunset", "2023-11-06 08:52:52.861506"),
    (6, "Where am I going?😏", "2023-11-06 08:55:40.931422"),
    (
        2,
        "I finished the project!!!\n"
        "https://gitlab.skillbox.ru/telitsin_andrei/python_advanced_diploma",
        "2023-11-06 08:58:46.917927",
    ),
    (
        3,
        "Poster for the new part!!! They say it will be out soon",
        "2023-11-06 09:01:08.857132",
    ),
]

LIKES: list[tuple[int, int]] = [
    (1, 2),
    (1, 3),
    (2, 2),
    (3, 6),
    (3, 5),
    (3, 2),
    (3, 3),
    (4, 6),
    (4, 4),
    (5, 4),
    (5, 2),
    (6, 2),
    (7, 5),
    (7, 6),
    (7, 2),
    (9, 3),
    (11, 3),
    (11, 2),
    (12, 5),
    (12, 6),
    (12, 2),
    (13, 5),
    (13, 6),
    (14, 3),
    (15, 3),
    (16, 2),
    (17, 4),
    (17, 5),
    (17, 6),
    (17, 2),
    (17, 3),
    (18, 6),
    (18, 2),
    (18, 4),
    (18, 3),
    (19, 4),
    (19, 3),
    (20, 2),
    (20, 3),
    (20, 5),
    (21, 3),
    (21, 2),
]


async def load_test_data() -> None:
    users_instance: list[UserModel] = [
        UserModel(name=i_data[0], api_key_hash=i_data[1]) for i_data in USERS
    ]

    followers_instance: list[UserFollowerModel] = [
        UserFollowerModel(user_id=i_data[0], follower_id=i_data[1])
        for i_data in FOLLOWERS
    ]

    media_instance: list[MediaModel] = [
        MediaModel(src=i_data[0], tweet_id=i_data[1], user_id=i_data[2])
        for i_data in MEDIA
    ]

    tweets_instance: list[TweetModel] = [
        TweetModel(
            user_id=i_data[0],
            content=i_data[1],
            create_at=datetime.strptime(i_data[2], DATE_FORMAT),
        )
        for i_data in TWEETS
    ]

    likes_instance: list[TweetLikeModel] = [
        TweetLikeModel(tweet_id=i_data[0], user_id=i_data[1]) for i_data in LIKES
    ]

    async with session_maker() as session:
        session.add_all(users_instance)
        await session.flush()

        session.add_all(followers_instance)
        session.add_all(tweets_instance)
        await session.flush()

        session.add_all(media_instance)
        session.add_all(likes_instance)
        await session.commit()
