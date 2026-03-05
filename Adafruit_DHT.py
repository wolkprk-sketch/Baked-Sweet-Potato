import random
import time

class DHTSensor:
    def __init__(self, pin, sensor_type="Unknown"):
        self._pin = pin
        self._sensor_type = sensor_type
        self._last_called = 0
        print(f"[Mock {self._sensor_type}] Initialized on pin {pin}")

    @property
    def temperature(self):
        self._check_timing()
        # Simulate a 10% chance of a checksum/timing error
        if random.random() < 0.10:
            raise RuntimeError("Checksum failure or timeout")
        return round(random.uniform(20.0, 30.0), 1)

    @property
    def humidity(self):
        self._check_timing()
        return round(random.uniform(30.0, 70.0), 1)

    def _check_timing(self):
        """DHT sensors need ~2 seconds between readings."""
        now = time.time()
        if now - self._last_called < 2.0:
            # We don't raise an error here usually, but the real 
            # hardware often returns the old cached value.
            pass
        self._last_called = now

    def read(self):
        return self.temperature, self.humidity

    def exit(self):
        print(f"[Mock {self._sensor_type}] Resources released.")

# Specific classes to match Adafruit's library structure
class DHT11(DHTSensor):
    def __init__(self, pin):
        super().__init__(pin, "DHT11")

class DHT22(DHTSensor):
    def __init__(self, pin):
        super().__init__(pin, "DHT22")

class AM2302(DHTSensor):
    def __init__(self, pin):
        super().__init__(pin, "AM2302")