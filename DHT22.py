# DHT22 Temperature & Humidity Sensor Reader

import time
import sys
from datetime import datetime

def try_adafruit_dht():
    """Try using adafruit_dht library"""
    try:
        import adafruit_dht
        import board
        
        # Try different pin names
        pin_attempts = ['D21', 'GPIO21', '21', 'D4', 'D17']
        
        for pin_name in pin_attempts:
            try:
                pin = getattr(board, pin_name)
                sensor = adafruit_dht.DHT22(pin)
                print(f"✓ Using adafruit_dht with pin {pin_name}")
                return sensor, "adafruit_dht"
            except AttributeError:
                continue
        
        # If no pin works, try creating pin manually
        try:
            import digitalio
            pin = digitalio.DigitalInOut(board.D21)
            sensor = adafruit_dht.DHT22(pin)
            print("✓ Using adafruit_dht with manual DigitalInOut")
            return sensor, "adafruit_dht"
        except:
            pass
            
    except ImportError:
        pass
    
    return None, None

def try_adafruit_DHT():
    """Try using Adafruit_DHT library (RPi.GPIO based)"""
    try:
        import Adafruit_DHT
        import RPi.GPIO as GPIO
        
        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = 21  # GPIO21
        
        # Test read
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        
        print("✓ Using Adafruit_DHT library (RPi.GPIO)")
        return (DHT_SENSOR, DHT_PIN), "Adafruit_DHT"
        
    except ImportError:
        pass
    
    return None, None

def main():
    """Main function"""
    print("=" * 60)
    print("DHT22 SENSOR READER - UNIVERSAL")
    print("=" * 60)
    
    print("\nTrying to initialize DHT22 sensor...")
    
    # Try adafruit_dht first
    sensor, method = try_adafruit_dht()
    
    # If that fails, try Adafruit_DHT
    if not sensor:
        sensor, method = try_adafruit_DHT()
    
    if not sensor:
        print("\n❌ Failed to initialize DHT22 sensor!")
        print("\nInstall required libraries:")
        print("1. For adafruit_dht: pip install adafruit-circuitpython-dht adafruit-blinka")
        print("2. For Adafruit_DHT: pip install Adafruit_DHT RPi.GPIO")
        sys.exit(1)
    
    print(f"\n✅ Initialized with method: {method}")
    print("Press Ctrl+C to stop\n")
    
    read_count = 0
    success_count = 0
    
    try:
        while True:
            read_count += 1
            
            try:
                if method == "adafruit_dht":
                    temperature = sensor.temperature
                    humidity = sensor.humidity
                else:  # Adafruit_DHT
                    DHT_SENSOR, DHT_PIN = sensor
                    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
                
                # Check if readings are valid
                if temperature is not None and humidity is not None:
                    success_count += 1
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    # Calculate success rate
                    success_rate = (success_count / read_count) * 100
                    
                    # Print reading
                    print(f"[{timestamp}] #{read_count:03d}: ", end="")
                    print(f"Temp: {temperature:5.1f}°C | ", end="")
                    print(f"Humidity: {humidity:5.1f}% | ", end="")
                    print(f"Success: {success_rate:5.1f}%")
                    
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for valid reading...")
                    
            except RuntimeError as e:
                print(f"Sensor error: {e}")
                
            except Exception as e:
                print(f"Unexpected error: {e}")
            
            # Wait between readings
            time.sleep(2.5)
            
    except KeyboardInterrupt:
        print("\n\nProgram stopped by user")
        
    finally:
        # Clean up
        if method == "adafruit_dht":
            sensor.exit()
            print("Sensor cleaned up")
        else:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
            print("GPIO cleaned up")
        
        # Statistics
        if read_count > 0:
            success_rate = (success_count / read_count) * 100
            print(f"\n📊 Final: {success_count}/{read_count} successful ({success_rate:.1f}%)")

if __name__ == "__main__":
    main()
