from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Note:
    summary: str
    description: str
    topic: str = None
