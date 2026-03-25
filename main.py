import asyncio
from DHT22 import DHT22
from Camera import Camera
from TTP223 import TTP223
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from Speaker import Speaker

class Gadget:
    def __init__(self):
        self.camera = Camera()
        self.dht22 = DHT22()
        self.speaker = Speaker()
        self.ttp223 = TTP223()
        self.i2c = I2C(sda=Pin(4), scl=Pin(5))
        self.display = SSD1306_I2C(128, 64, self.i2c)
    
    async def touch_monitor(self):
        while True:
            try:
                if self.ttp223.is_touched():
                    self.speaker.speak("Current temperature is {:.1f} degrees Celsius and humidity is {:.1f} percent.".format(self.temperature_degree, self.humidity))
                    self.speaker.speak("There are currently {} people detected.".format(self.people_count))
            except Exception as e:
                print(f"Error reading touch sensor: {e}")

            await asyncio.sleep(0.1)
    
    async def sensor_monitor(self):
        while True:
            try:
                self.temperature_degree, self.humidity = self.dht22.read()
                self.people_count = self.camera.num_of_people()
                print(f"Temperature: {self.temperature_degree:.1f}°C, Humidity: {self.humidity:.1f}%, People Count: {self.people_count}")
                self.display.fill(0)
                self.display.text(f"Temp: {self.temperature_degree:.1f}C", 0, 0, 1)
                self.display.text(f"Hum: {self.humidity:.1f}%", 0, 20, 1)
                self.display.text(f"People: {self.people_count}", 0, 40, 1)
                self.display.show()
            except Exception as e:
                print(f"Error reading sensors: {e}")
            await asyncio.sleep(2)

    def __exit__(self):
        print("Exiting program...")
        self.camera.__exit__()
        self.dht22.__exit__()
        self.ttp223.__exit__()
        self.display.poweroff()





if __name__ == '__main__':
    gadget = Gadget()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(
            gadget.touch_monitor(),
            gadget.sensor_monitor()
        ))
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        gadget.__exit__()
        loop.close()