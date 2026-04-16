from luma.core.interface.serial import spi
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw, ImageFont

<<<<<<< HEAD
COMMANDS = ["show menu", "take photo", "take video", "hey glasses, (question here)"]
=======
COMMANDS = [
    "take photo",
    "take video",
    "question, ..?",
]
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d


class OLEDHandler:
    initialized: bool = False
    serial: spi
    device: ssd1309
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont

    def __init__(self):
        self.init()
<<<<<<< HEAD
=======
        self._display_menu()
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d

    @classmethod
    def init(cls) -> None:
        if cls.initialized:
            return

        cls.serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)
        cls.device = ssd1309(cls.serial, width=128, height=64)
        cls.font = ImageFont.load_default()
        cls.initialized = True

    @classmethod
<<<<<<< HEAD
    def display_ai_answer(cls, answer: str) -> None:
        cls.init()
        cls.device.clear()
        image = Image.new("1", (cls.device.width, cls.device.height))
        draw = ImageDraw.Draw(image)
        draw.text((10, 12), answer, font=cls.font, fill=255)
=======
    def _wrap_text(cls, text: str, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = word if not current_line else f"{current_line} {word}"
            bbox = draw.textbbox((0, 0), test_line, font=cls.font)
            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    @classmethod
    def display_text(cls, text: str) -> None:
        cls.init()
        cls.device.clear()

        image = Image.new("1", (cls.device.width, cls.device.height))
        draw = ImageDraw.Draw(image)

        padding_x = 10
        padding_y = 6
        line_spacing = 2
        max_width = cls.device.width - (padding_x * 2)

        # Estimate line height from font
        bbox = draw.textbbox((0, 0), "Ay", font=cls.font)
        line_height = (bbox[3] - bbox[1]) + line_spacing

        lines = cls._wrap_text(text, max_width, draw)

        y = padding_y
        for line in lines:
            if y + line_height > cls.device.height:
                break  # stop drawing if screen is full
            draw.text((padding_x, y), line, font=cls.font, fill=255)
            y += line_height

        cls.device.display(image)
        print("[oled] displayed text")
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d

    def _display_menu(self) -> None:
        self.device.clear()
        image = Image.new("1", (self.device.width, self.device.height))
        draw = ImageDraw.Draw(image)
<<<<<<< HEAD
        pos = 12
        for command in COMMANDS:
            draw.text((10, pos), command, font=self.font, fill=255)
            pos += 18

    def handle_command(self, cmd: str) -> None:
        if "show menu" in cmd:
            self._display_menu()


handler = OLEDHandler()
OLEDHandler.display_ai_answer("hello")
=======
        pos = 8
        for command in COMMANDS:
            draw.text((10, pos), command, font=self.font, fill=255)
            pos += 14

        self.device.display(image)
        print("[oled] displayed menu")

    def handle_command(self, cmd: str) -> None:
        if "show menu" in cmd:
            self._display_menu()
>>>>>>> c2d09b27652a30d8f05a6905ddd438a02cd5ea0d
