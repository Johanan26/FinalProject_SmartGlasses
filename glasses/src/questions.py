from urllib.parse import urljoin
import requests
import os


class QuestionHandler:
    def __init__(self):
        pass

    def handle_command(self, cmd: str) -> None:
        url = os.environ.get("BACKEND_URL")
        request = requests.post(urljoin(url, "ask_question"), json={
            "data": cmd
        })
        
        # TODO: print this to some form of screen :()
        print(request.json())