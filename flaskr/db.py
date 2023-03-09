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


class GameLibrary(list[Game]):
    def __init__(self) -> None:
        self.append(Game("Tetris", "Puzzle", "Atari"))
        self.append(Game("Skyrim", "RPG", "PS3"))
        self.append(Game("Crash Bandicoot", "Platform", "PS1"))

    def create(self, a_name: str, a_genre: str, a_platform: str) -> None:
        game = Game(a_name, a_genre, a_platform)
        self.append(game)


game_library = GameLibrary()
