import random

# Constants to mimic the real library
DHT11 = 11
DHT22 = 22
AM2302 = 22

def read(sensor, pin, retries=5, delay_seconds=2):
    """
    Mimics the read_retry method. 
    Returns a tuple of (humidity, temperature).
    """
    # You can customize these ranges to test your specific logic
    if sensor == DHT11:
        # DHT11 is less precise (integers)
        humidity = random.randint(20, 80)
        temperature = random.randint(0, 50)
    else:
        # DHT22/AM2302 is more precise (floats)
        humidity = round(random.uniform(10.0, 90.0), 1)
        temperature = round(random.uniform(-40.0, 80.0), 1)

    # Optional: Simulate an occasional failed read (None, None)
    if random.random() < 0.05: 
        return None, None

    return humidity, temperature