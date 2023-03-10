class Game:
    def __init__(self, a_name: str, a_genre: str, a_platform: str) -> None:
        self.__name = a_name
        self.__genre = a_genre
        self.__platform = a_platform

    @property
    def name(self) -> str:
        return self.__name

    @property
    def genre(self) -> str:
        return self.__genre

    @property
    def platform(self) -> str:
        return self.__platform


class Games(list[Game]):
    def __init__(self) -> None:
        self.append(Game("Tetris", "Puzzle", "Atari"))
        self.append(Game("Skyrim", "RPG", "PS3"))
        self.append(Game("Crash Bandicoot", "Platform", "PS1"))

    def create(self, a_name: str, a_genre: str, a_platform: str) -> None:
        game = Game(a_name, a_genre, a_platform)
        self.append(game)


class User:
    def __init__(self, a_name: str, a_username: str, a_password: str) -> None:
        self.__name = a_name
        self.__username = a_username
        self.__password = a_password

    @property
    def name(self) -> str:
        return self.__name

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password


class Users(list[User]):
    def __init__(self) -> None:
        self.append(User("Gabriel Alves", "alvesgf16", "alohomora"))
        self.append(User("Camilla Bastos", "cams", "paozinho"))
        self.append(User("Guilherme Ferreira", "cake", "python_eh_vida"))

    def get_by_username(self, a_username: str) -> User:
        usernames = [user.username for user in self]
        user_index = usernames.index(a_username)
        return self[user_index]


class Database:
    def __init__(self) -> None:
        self.__games = Games()
        self.__users = Users()

    @property
    def games(self) -> Games:
        return self.__games

    @property
    def users(self) -> Users:
        return self.__users


db = Database()
