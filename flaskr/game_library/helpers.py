import time

from flask import current_app
from werkzeug.datastructures import FileStorage


class GameCoverUploader:
    def __init__(self, a_game_id: int) -> None:
        self.game_id = a_game_id
        self.upload_path = current_app.config["UPLOAD_PATH"]

    def upload_cover_file(self, a_cover_art: FileStorage) -> None:
        timestamp = time.time()
        a_cover_art.save(
            f"{self.upload_path}/cover{self.game_id}-{timestamp}.jpg"
        )
