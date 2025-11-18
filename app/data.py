from typing import List

from .models import Movietop, User

movies_list: List[Movietop] = [
    Movietop(
        id=1,
        name="Криминальное чтиво",
        cost=8_000_000,
        director="Квентин Тарантино",
        watched=True,
    ),
    Movietop(
        id=2,
        name="Крестный отец",
        cost=6_000_000,
        director="Фрэнсис Форд Коппола",
        watched=True,
    ),
    Movietop(
        id=3,
        name="Темный рыцарь",
        cost=185_000_000,
        director="Кристофер Нолан",
        watched=True,
    ),
    Movietop(
        id=4,
        name="Список Шиндлера",
        cost=22_000_000,
        director="Стивен Спилберг",
        watched=True,
    ),
    Movietop(
        id=5,
        name="Форрест Гамп",
        cost=55_000_000,
        director="Роберт Земекис",
        watched=True,
    ),
    Movietop(
        id=6,
        name="Властелин колец: Возвращение короля",
        cost=94_000_000,
        director="Питер Джексон",
        watched=True,
    ),
    Movietop(
        id=7,
        name="Титаник",
        cost=200_000_000,
        director="Джеймс Кэмерон",
        watched=True,
    ),
    Movietop(
        id=8,
        name="Интерстеллар",
        cost=165_000_000,
        director="Кристофер Нолан",
        watched=True,
    ),
    Movietop(
        id=9,
        name="Аватар",
        cost=237_000_000,
        director="Джеймс Кэмерон",
        watched=True,
    ),
    Movietop(
        id=10,
        name="Побег из Шоушенка",
        cost=25_000_000,
        director="Фрэнк Дарабонт",
        watched=True,
    ),
]

users_list: List[User] = [
    User(username="admin", password="secret"),
]

