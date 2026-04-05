from luma.core.interface.serial import spi
from luma.oled.device import ssd1309
from PIL import Image, ImageDraw, ImageFont
from time import sleep

# SPI setup:
# port=0  -> SPI0
# device=0 -> CE0
# gpio_DC=24  -> GPIO24
# gpio_RST=25 -> GPIO25
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25)

# Create display object
device = ssd1309(serial, width=128, height=64)

# Clear screen
device.clear()

# Create a blank image
image = Image.new("1", (device.width, device.height))
draw = ImageDraw.Draw(image)

# Optional border
draw.rectangle((0, 0, device.width - 1, device.height - 1), outline=255, fill=0)

# Use default font
font = ImageFont.load_default()

# Draw some text
draw.text((10, 12), "Hello Pookie!", font=font, fill=255)
draw.text((10, 30), "OLED test OK", font=font, fill=255)

# Send image to display
device.display(image)

sleep(10)

# Clear after 10 seconds
device.clear()