from luma.core.interface.serial import spi
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw, ImageFont

COMMANDS = [
    "take photo",
    "take video",
    "question, ..?",
]


class OLEDHandler:
    initialized: bool = False
    serial: spi
    device: ssd1309
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont

    def __init__(self):
        self.init()
        self._display_menu()

    @classmethod
    def init(cls) -> None:
        if cls.initialized:
            return

        cls.serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
        cls.device = ssd1309(cls.serial, width=128, height=64)
        cls.font = ImageFont.load_default()
        cls.initialized = True

    @classmethod
    def display_text(cls, text: str) -> None:
        cls.init()
        cls.device.clear()
        image = Image.new("1", (cls.device.width, cls.device.height))
        draw = ImageDraw.Draw(image)
        draw.text((10, 12), text, font=cls.font, fill=255)
        cls.device.display(image)
        print("[oled] displayed text")

    def _display_menu(self) -> None:
        self.device.clear()
        image = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(image)
        pos = 8
        for command in COMMANDS:
            draw.text((10, pos), command, font=self.font, fill=255)
            pos += 14

        self.device.display(image)
        print("[oled] displayed menu")

    def handle_command(self, cmd: str) -> None:
        if "show menu" in cmd:
            self._display_menu()
