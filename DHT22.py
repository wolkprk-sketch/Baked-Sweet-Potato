# DHT22 Temperature & Humidity Sensor Reader

import time
import sys
from datetime import datetime

class DHT22:
    def __init__(self):
        print("Trying to initialize DHT22 sensor...")

        # Try adafruit_dht first
        self.try_adafruit_dht()

        # If that fails, try Adafruit_DHT
        if not self.sensor:
            self.try_adafruit_DHT()

        if not self.sensor:
            print("\nFailed to initialize DHT22 sensor!")
            sys.exit(1)

    def try_adafruit_dht(self):
        # Try using adafuit_dht library
        try:
            import adafruit_dht
            import board
            
            # Try different pin names
            pin_attempts = ['D21', 'GPIO21', '21', 'D4', 'D17']

            for pin_name in pin_attempts:
                try:
                    pin = getattr(board, pin_name)
                    self.sensor = adafruit_dht.DHT22(pin)
                    self.method = "adafruit_dht"
                    print(f"✓ Using adafruit_dht with pin {pin_name}")
                    return 0
                
                except AttributeError:
                    continue
            
            # If no pin works, try creating manually
            try:
                import digitalio
                pin = digitalio.DigitalInOut(board.D21)
                self.sensor = adafruit_dht.DHT22(pin)
                self.method = "adafruit_dht"
                print("✓ Using adafruit_dht with manual DigitalInOut")
                return 0
            
            except:
                pass
        
        except ImportError:
            pass

        self.sensor, self.method = None, None
        return 0
    
    def try_adafruit_DHT(self):
        # Try using Adafruit_DHT library (RPi.GPIO based)
        try:
            import Adafruit_DHT
            import RPi.GPIO as GPIO

            DHT_SENSOR = Adafruit_DHT.DHT22
            DHT_PIN = 21    # GPIO21

            # Test read
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

            self.sensor = (DHT_SENSOR, DHT_PIN)
            self.method = "Adafruit_DHT"

            print("✓ Using Adafruit_DHT library (RPi.GPIO)")
            return 0
        
        except ImportError:
            pass

        self.sensor, self.method = None, None
        return 0
    
    def read(self):
        try:
            if self.method == "adafruit_dht":
                temperature = self.sensor.temperature
                humidity = self.sensor.humidity
            
            else: # Adafruit_DHT
                import Adafruit_DHT
                DHT_SENSOR, DHT_PIN = self.sensor
                humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

            return temperature, humidity
        
        except RuntimeError as e:
            print(f"Sensor error: {e}")
        
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        return None, None
    
    def __exit__(self):
        if self.method == "adafruit_dht":
            self.sensor.exit()
            print("DHT22 cleaned up")
        else:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
            print("DHT22 cleaned up")


def main():
    dht22 = DHT22()
    while True:
        try:
            temperature, humidity = dht22.read()
            if temperature is not None and humidity is not None:
                print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
            else:
                print("Failed to read from DHT22 sensor.")
            time.sleep(2)
        except KeyboardInterrupt:
            print("Exiting program...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            dht22.__exit__()
            sys.exit(0)
if __name__ == "__main__":
    main()
