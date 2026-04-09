from luma.core.interface.serial import spi
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw, ImageFont

COMMANDS = ["show menu", "take photo", "take video", "hey glasses, (question here)"]


class OLEDHandler:
    initialized: bool = False
    serial: spi
    device: ssd1309
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont

    def __init__(self):
        self.init()

    @classmethod
    def init(cls) -> None:
        if cls.initialized:
            return

        cls.serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
        cls.device = ssd1309(cls.serial, width=128, height=64)
        cls.font = ImageFont.load_default()
        cls.initialized = True

    @classmethod
    def display_ai_answer(cls, answer: str) -> None:
        cls.init()
        cls.device.clear()
        image = Image.new("1", (cls.device.width, cls.device.height))
        draw = ImageDraw.Draw(image)
        draw.text((10, 12), answer, font=cls.font, fill=255)

    def _display_menu(self) -> None:
        self.device.clear()
        image = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(image)
        pos = 12
        for command in COMMANDS:
            draw.text((10, pos), command, font=self.font, fill=255)
            pos += 18

    def handle_command(self, cmd: str) -> None:
        if "show menu" in cmd:
            self._display_menu()


handler = OLEDHandler()
OLEDHandler.display_ai_answer("hello")
