"""
Mock implementation of the SSD1306 OLED driver for MicroPython.
"""

class SSD1306:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        # Create a virtual buffer (0 for off, 1 for on)
        self.buffer = [[0 for _ in range(width)] for _ in range(height)]
        print(f"[Mock OLED] Initialized {width}x{height}")

    def init_display(self):
        pass

    def poweroff(self):
        print("[Mock OLED] Power Off")

    def poweron(self):
        print("[Mock OLED] Power On")

    def contrast(self, contrast):
        print(f"[Mock OLED] Contrast set to {contrast}")

    def invert(self, invert):
        print(f"[Mock OLED] Invert set to {invert}")

    def rotate(self, rotate):
        print(f"[Mock OLED] Rotate set to {rotate}")

    def show(self):
        """Prints a simplified ASCII version of the buffer to the console."""
        print("+" + "-" * self.width + "+")
        #for row in self.buffer:
        #    line = "".join(["#" if pixel else " " for pixel in row])
        #    print(f"|{line}|")
        #print("+" + "-" * self.width + "+")

    def fill(self, col):
        self.buffer = [[col for _ in range(self.width)] for _ in range(self.height)]

    def pixel(self, x, y, col):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = col

    def text(self, string, x, y, col=1):
        print(f"[Mock OLED] Text at ({x},{y}): '{string}'")
        # In a real mock, you'd draw a font bitmask here. 
        # For simplicity, we just log the text.

class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        super().__init__(width, height, external_vcc)

class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        super().__init__(width, height, external_vcc)