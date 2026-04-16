import os
from urllib.parse import urljoin

import requests

<<<<<<< HEAD
from glasses.src.oled import OLEDHandler
=======
from .oled import OLEDHandler
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d


class QuestionHandler:
    def __init__(self):
        pass

    def handle_command(self, cmd: str) -> None:
        url = os.environ.get("BACKEND_URL")

        if not url:
            return

        request = requests.post(urljoin(url, "ask_question"), json={"data": cmd})

        # TODO: print this to some form of screen :()
<<<<<<< HEAD
        OLEDHandler.display_ai_answer(request.json())
=======
        OLEDHandler.display_text(request.json())
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d
