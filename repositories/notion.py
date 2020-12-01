import logging
from concurrent.futures.thread import ThreadPoolExecutor

from notion.block import TextBlock
from notion.client import NotionClient

from note import Note
from repositories.base import NotesRepository

logger = logging.getLogger()


class NotionNotesRepository(NotesRepository):
    DB_URL = "https://www.notion.so/a57dc4146a5b4266a99033dbdfddb9a3?v=dd0b5bfbb7504bcb939f73fff30cad00"

    def __init__(self, token: str) -> None:
        super().__init__()
        logger.info("Connecting to Notion")
        self.client = NotionClient(token_v2=token)

        logger.info("Connecting to database")
        self.db = self.client.get_collection_view(self.DB_URL)

        self.executor = ThreadPoolExecutor(1)

    def save(self, note: Note):
        self.executor.submit(self._save_task, note)

    def _save_task(self, note: Note):
        logger.info("Saving note to notion")
        row = self.db.collection.add_row()
        row.name = note.summary

        for line in note.description.splitlines():
            row.children.add_new(TextBlock, title=line)

        logger.info(f"Note saved with summary '{note.summary}'")
