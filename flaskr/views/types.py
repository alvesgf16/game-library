from typing import Union

from werkzeug import Response

from flaskr.models import Game as GameModel, User as UserModel

Game = GameModel
Renderable = Union[Response, str]
User = UserModel
