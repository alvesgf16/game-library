from typing import Callable, Union

from werkzeug import Response

from flaskr.models import Game as GameModel, User as UserModel

Game = GameModel
IntConverter = dict[str, int]
Renderable = Union[Response, str]
Route = Callable[..., Renderable]
User = UserModel
