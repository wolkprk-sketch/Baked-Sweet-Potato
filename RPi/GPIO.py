# RPi/GPIO.py

# Pin Numbering Systems
BOARD = "BOARD"
BCM = "BCM"

# Pin States
OUT = "OUT"
IN = "IN"
HIGH = 1
LOW = 0

# Pull Up/Down
PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2

def setmode(mode):
    print(f"[GPIO] Mode set to: {mode}")

def setwarnings(flag):
    print(f"[GPIO] Warnings set to: {flag}")

def setup(pin, mode, pull_up_down=PUD_OFF):
    print(f"[GPIO] Pin {pin} configured as {mode}")

def output(pin, state):
    status = "HIGH" if state else "LOW"
    print(f"[GPIO] Output Pin {pin} -> {status}")

def input(pin):
    print(f"[GPIO] Reading Pin {pin} (Returning LOW/0)")
    return 0

def cleanup():
    print("[GPIO] Cleaning up all channels...")