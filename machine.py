class Pin:
    IN = 0
    OUT = 1
    PULL_UP = 1
    PULL_DOWN = 2

    def __init__(self, id, mode=-1, pull=-1, value=None):
        self.id = id
        self.mode = mode
        self.pull = pull
        self._value = value if value is not None else 0
        print(f"[Mock] Pin {id} initialized (Mode: {mode})")

    def value(self, val=None):
        if val is not None:
            self._value = val
            print(f"[Mock] Pin {self.id} set to {val}")
        return self._value

    def on(self):
        self.value(1)

    def off(self):
        self.value(0)


class I2C:
    def __init__(self, id=-1, scl=None, sda=None, freq=400000):
        self.id = id
        self.scl = scl
        self.sda = sda
        self.freq = freq
        # Mock 'devices' on the bus: {address: bytearray_data}
        self._devices = {0x3C: bytearray([0x00])} 
        print(f"[Mock] I2C {id} initialized at {freq}Hz")

    def scan(self):
        print(f"[Mock] Scanning I2C bus...")
        return list(self._devices.keys())

    def writeto(self, addr, data, stop=True):
        print(f"[Mock] I2C Write to {hex(addr)}: {list(data)}")
        self._devices[addr] = bytearray(data)

    def readfrom(self, addr, nbytes, stop=True):
        data = self._devices.get(addr, bytearray([0] * nbytes))
        print(f"[Mock] I2C Read from {hex(addr)}: {list(data)}")
        return data

    def writeto_mem(self, addr, memaddr, data):
        print(f"[Mock] I2C Write to {hex(addr)} at mem {hex(memaddr)}: {list(data)}")

    def readfrom_mem(self, addr, memaddr, nbytes):
        print(f"[Mock] I2C Read from {hex(addr)} at mem {hex(memaddr)}")
        return bytearray([0xFF] * nbytes)