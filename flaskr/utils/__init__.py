from flask import request, session

from .cover_uploader import GameCoverUploader
from .form_validators import GameForm, UserForm

__all__ = ["GameCoverUploader", "GameForm", "UserForm"]


def is_post_request() -> bool:
    return request.method == "POST"


def is_user_logged_in() -> bool:
    return "logged_in_user" in session
