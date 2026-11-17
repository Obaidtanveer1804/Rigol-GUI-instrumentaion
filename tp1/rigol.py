import time
import pyvisa


class Rigol:
    """Any Rigol USB instrument: connect, write, read.
    `key` is the part of the VISA name that identifies the device
    (vendor id::product id), so two instruments can be told apart."""

    def __init__(self, key):
        self.key = key
        self.inst = None

    def connect(self):
        rm = pyvisa.ResourceManager('@py')
        name = [r for r in rm.list_resources('USB?*::INSTR') if self.key in r][0]
        self.inst = rm.open_resource(name)

    def write(self, cmd):
        self.inst.write(cmd)

    def read(self):
        return self.inst.read().strip()


class Generator(Rigol):
    """DG1022 function generator (USB id 0x0400:0x09c4 = 1024::2500)."""

    def __init__(self):
        super().__init__("::1024::2500::")

    def apply(self, signal, freq, amplitude, offset, phase):
        """Send waveform settings to CH1 (APPLy command + PHASe)."""
        names = {"SINE": "SIN", "SQUARE": "SQU", "RAMP": "RAMP", "DC": "DC"}
        if signal == "DC":
            self.write(f"APPL:DC DEF,DEF,{offset}")
        else:
            self.write(f"APPL:{names[signal]} {freq},{amplitude},{offset}")
        time.sleep(0.5)  # the DG1022 is slow: it drops a command sent right after another
        self.write(f"PHAS {phase}")


class Scope(Rigol):
    """DS1000Z oscilloscope (USB id 0x1ab1:0x04ce = 6833::1230)."""

    def __init__(self):
        super().__init__("::6833::1230::")

    def measure(self, item, channel="CHANnel1"):
        """Ask for one measurement, e.g. FREQuency, VPP (read the answer with read())."""
        self.write(f":MEASure:ITEM? {item},{channel}")
        print("measuring item", item, "channel", channel )
