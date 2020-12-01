import logging
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from notion.block import TextBlock
from notion.client import NotionClient

from note import Note
from repositories.base import NotesRepository

logger = logging.getLogger()


class NotionNotesRepository(NotesRepository):
    NOTES_URL = "https://www.notion.so/a57dc4146a5b4266a99033dbdfddb9a3?v=dd0b5bfbb7504bcb939f73fff30cad00"
    TOPICS_URL = "https://www.notion.so/8ba2c4f400854571843a5e1ebe07a63d?v=f55b5d0ffb5148c68c24431d4af80a8e"

    def __init__(self, token: str) -> None:
        super().__init__()
        logger.info("Connecting to Notion")
        self.client = NotionClient(token_v2=token)

        logger.info("Connecting to database")
        self.notes_db = self.client.get_collection_view(self.NOTES_URL)

        logger.info("Loading topics")
        self.topics_db = self.client.get_collection_view(self.TOPICS_URL)
        self.topics_cache = {topic.name: topic for topic in self.topics_db.collection.get_rows()}

        self.executor = ThreadPoolExecutor(1)

    def topics(self) -> List[str]:
        return list(self.topics_cache.keys())

    def save(self, note: Note):
        self.executor.submit(self._save_task, note)

    def _save_task(self, note: Note):
        logger.info("Saving note to notion")
        row = self.notes_db.collection.add_row()
        row.name = note.summary

        for line in note.description.splitlines():
            row.children.add_new(TextBlock, title=line)

        row.topics = [self.topics_cache[note.topic]]

        logger.info(f"Note saved with summary '{note.summary}'")
