from pathlib import Path

from repositories.base import NotesRepository
from note import Note


class FileNotesRepository(NotesRepository):

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path

    def save(self, note: Note):
        with open(self.path, "a") as file:
            file.write(note.to_json())
            file.write("\n")
