import logging
from pathlib import Path

from django.conf import settings
from tika_client import TikaClient

from content.models import Document
from plugin.core import BasePlugin


class TikaClientPlugin(BasePlugin):
    def __init__(self) -> None:
        super().__init__()
        self.client = TikaClient(tika_url='http://192.168.124.18:9998', log_level=logging.DEBUG)

    def run(self, doc: Document) -> str:
        root_path = Path(settings.STORE_PATH)
        file_path = root_path.joinpath(doc.path)
        mime_type = doc.mime_type
        parsed = self.client.tika.as_text.from_file(file_path, mime_type=mime_type)
        print(parsed)
        print(dir(parsed))
        print(parsed.created)
        print(parsed.language)
        print(parsed.last_author)
        print(parsed.modified)
        print(parsed.title)
        print(parsed.page_count)
        print(parsed.type)
        print(parsed.xmp_created)
        print(parsed.character_count)
        print(parsed.revision)
        print(parsed.parsers)
        return {'content': parsed.content, 'page_count': parsed.page_count}
