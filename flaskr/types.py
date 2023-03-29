from typing import Callable, Union

from werkzeug import Response

IntConverter = dict[str, int]
Renderable = Union[Response, str]
Route = Callable[..., Renderable]
