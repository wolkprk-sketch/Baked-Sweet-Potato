import RPi.GPIO as GPIO
import time

class TTP223:
    def __init__(self, touch_pin=18):
        
        print("Trying to Initialize TTP223...")
        try:
            import RPi.GPIO as GPIO
            self.touch_pin = touch_pin
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.touch_pin, GPIO.IN)
        except ImportError:
            pass
        print("TTP223 initialized!")

    def is_touched(self):
        import RPi.GPIO as GPIO
        if GPIO.input(self.touch_pin):
            return True
        return False
    
    def __exit__(self):
        GPIO.cleanup()

def main():
    ttp223 = TTP223()
    try:
        while True:
            if ttp223.is_touched():
                print("Touch detected!")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting program...")
        ttp223.__exit__()


if __name__ == '__main__':
    main()