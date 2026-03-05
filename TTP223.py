import RPi.GPIO as GPIO
import time
touch_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(touch_pin , GPIO.IN)

print("Touch sensor running... (Ctrl+C to stop)")

try:
    while True:
        if GPIO.input(touch_pin ):
            print("TOUCHED!")
        else:
            print(".")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nDone")
    GPIO.cleanup()