from urllib.parse import urljoin
from typing import TYPE_CHECKING

import requests
import os

if TYPE_CHECKING:
    from microphone import RazeListener
    
class QuestionHandler:
    def __init__(self, listener: RazeListener):
        self.listener = listener
        
    def run(self):
        while True:
            cmd = self.listener.get_command()
            
            if not cmd:
                continue
            
            cmd = cmd.lower()

            url = os.environ.get("BACKEND_URL")
            
            if "question" in cmd:
                request = requests.post(urljoin(url, "/ask_question"), {
                    "data": cmd
                })
                
                # TODO: print this to some form of screen :()
                print(request.json())