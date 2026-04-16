import os
from urllib.parse import urljoin

import requests

from src.oled import OLEDHandler


class QuestionHandler:
    def __init__(self):
        pass

    def handle_command(self, cmd: str) -> None:
        url = os.environ.get("BACKEND_URL")

        if not url:
            return

        request = requests.post(urljoin(url, "ask_question"), json={"data": cmd})

        OLEDHandler.display_ai_answer(request.json())
        OLEDHandler.display_text(request.json())
