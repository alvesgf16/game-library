import os
import time

from flask import current_app
from werkzeug.datastructures import FileStorage


class GameCoverUploader:
    def __init__(self, a_game_id: int) -> None:
        self.game_id = a_game_id
        self.upload_path = current_app.config["UPLOAD_PATH"]

    @property
    def uploaded_files(self) -> list[str]:
        return os.listdir(self.upload_path)

    def upload_cover_file(self, a_cover_art: FileStorage) -> None:
        timestamp = time.time()
        a_cover_art.save(
            f"{self.upload_path}/cover{self.game_id}-{timestamp}.jpg"
        )

    def retrieve_uploaded_cover_filename(self) -> str:
        return next(
            (
                filename
                for filename in self.uploaded_files
                if f"cover{self.game_id}" in filename
            ),
            "default_cover.jpg",
        )

    def delete_cover_file(self) -> None:
        filename = self.retrieve_uploaded_cover_filename()
        if self.__is_not_default_cover(filename):
            self.__delete_file(filename)

    def __is_not_default_cover(self, a_filename: str) -> bool:
        return a_filename != "default_cover.jpg"

    def __delete_file(self, a_filename: str) -> None:
        os.remove(os.path.join(self.upload_path, a_filename))
