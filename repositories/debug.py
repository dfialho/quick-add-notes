from repositories.base import NotesRepository
from note import Note


class DebugNotesRepository(NotesRepository):

    def save(self, note: Note):
        print(note.to_json())
