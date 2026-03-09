# RPi/GPIO.py

# Pin Numbering Modes
BOARD = 10
BCM = 11

# Pin Directions
OUT = 0
IN = 1

# Voltage Levels
HIGH = 1
LOW = 0

# Pull Up/Down
PUD_OFF = 20
PUD_UP = 21
PUD_DOWN = 22

def setmode(mode):
    mode_str = "BCM" if mode == BCM else "BOARD"
    print(f"[GPIO] Mode set to {mode_str}")

def setup(channel, direction, pull_up_down=PUD_OFF):
    dir_str = "OUT" if direction == OUT else "IN"
    print(f"[GPIO] Setup Pin {channel} as {dir_str}")

def output(channel, state):
    state_str = "HIGH" if state == HIGH else "LOW"
    print(f"[GPIO] Output Pin {channel} -> {state_str}")

def input(channel):
    import random
    # Randomly simulate a button press or sensor trigger
    val = random.choices([HIGH, LOW], weights=[0.1, 0.9])[0]  # 10% chance of HIGH
    return val

def cleanup():
    print("[GPIO] Cleaning up pins...")