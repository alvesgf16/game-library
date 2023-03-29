from flask import request

from .cover_uploader import GameCoverUploader
from .form_validators import GameForm, UserForm

__all__ = ["GameCoverUploader", "GameForm", "UserForm"]


def is_post_request() -> bool:
    return request.method == "POST"
