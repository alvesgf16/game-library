import os
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

    def retrieve_uploaded_cover_filename(self) -> str:
        uploaded_files = os.listdir(self.upload_path)
        return next(
            (
                filename
                for filename in uploaded_files
                if f"cover{self.game_id}" in filename
            ),
            "default_cover.jpg",
        )

    def delete_cover_file(self) -> None:
        filename = self.retrieve_uploaded_cover_filename()
        if filename != "default_cover.jpg":
            os.remove(os.path.join(self.upload_path, filename))
