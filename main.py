import os
import time
import tempfile
import pandas as pd

from argparse import ArgumentParser
from ina219 import INA219

TEMP_DIR = tempfile.gettempdir()
DEFAULT_FILE = "battery_info.data"

def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", default=DEFAULT_FILE,
                        help=f"output data file, default to {DEFAULT_FILE}")
    parser.add_argument("-d", "--directory", default=TEMP_DIR,
                        help=f"output directory, default to {TEMP_DIR}")
    parser.add_argument("-r", "--frequency", default=5,
                        help="frequency, default to 2 seconds")
    parser.add_argument("-a", "--address", default=0x42,
                        help="i2c bus address, default to 0x42")

    args = parser.parse_args()

    ina219 = INA219(addr=args.address)
    while True:
        time.sleep(args.frequency)
        bus_voltage = ina219.get_bus_voltage()
        current = ina219.get_current() / 1000  
        power = ina219.get_power()
        p = (bus_voltage - 6) / 2.4 * 100
        if(p > 100):
            p = 100
        if(p < 0):
            p = 0
        filename = os.path.join(args.directory, args.file)
        print(f"writing to {filename}")
        df = pd.DataFrame([{
            "voltage(V)": f"{bus_voltage:.3f}",
            "current(A)": f"{current:.6f}",
            "power(W)": f"{power:.3f}",
            "battery(%)": f"{p:.1f}"
            }])
        df.to_csv(filename, index=False)
        # with open(os.path.join(args.directory, args.file), "w") as f:
        #     # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
        #     f.write(f"voltage={bus_voltage:.3f}V\n")
        #     f.write(f"current={current:.6f}A\n")
        #     f.write(f"power={power:.3f}W\n")
        #     f.write(f"battery={p:.1f}%\n")

if __name__=='__main__':
    main()
