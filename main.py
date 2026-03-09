import asyncio
from DHT22 import DHT22
from Camera import Camera
from TTP223 import TTP223
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import sys
import RPi.GPIO as GPIO

async def touch_monitor(ttp223):
    while True:
        try:
            if ttp223.is_touched():
                print("Touch detected!")
        except Exception as e:
            print(f"Error reading touch sensor: {e}")

        await asyncio.sleep(0.1)

async def sensor_monitor(dht22, camera, display):
    while True:
        try:
            temperature_degree, humidity = dht22.read()
            people_count = camera.num_of_people()
            print(f"Temperature: {temperature_degree:.1f}°C, Humidity: {humidity:.1f}%, People Count: {people_count}")

            display.fill(0)
            display.text(f"Temp: {temperature_degree:.1f}C", 0, 0, 1)
            display.text(f"Hum: {humidity:.1f}%", 0, 20, 1)
            display.text(f"People: {people_count}", 0, 40, 1)
            display.show()
        except Exception as e:
            print(f"Error reading sensors: {e}")
        await asyncio.sleep(2)
async def main():
    # Initialize all components
    camera = Camera()
    dht22 = DHT22()
    ttp223 = TTP223()
    i2c = I2C(sda=Pin(4), scl=Pin(5))
    display = SSD1306_I2C(128, 64, i2c)
    

    display.text("Hello World!", 40, 0, 1)
    display.text("OLED Test", 40, 20, 1)
    display.text("Initializing...", 40, 40, 1)
    display.show()
    
    # Start concurrent tasks
    try:
        await asyncio.gather(
            touch_monitor(ttp223),
            sensor_monitor(dht22, camera, display)
        )
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting program...")
        camera.__exit__()
        dht22.__exit__()
        GPIO.cleanup()
        ttp223.__exit__()
        display.poweroff()



if __name__ == '__main__':
    print(0)
    asyncio.run(main())