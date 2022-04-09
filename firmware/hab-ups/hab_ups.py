from pijuice import PiJuice, PiJuiceInterface
from time import sleep


def monitor():
    ifs = PiJuiceInterface()
    pj = PiJuice()

    while True:
        
        status = pj.status.GetChargeLevel()
        voltage = pj.status.GetBatteryVoltage()
        current = pj.status.GetBatteryCurrent()
        temp = pj.status.GetBatteryTemperature()
        print(status)
        print(voltage)
        print(current)
        print(temp)
        print("")
        sleep(1)






if __name__ == "__main__":
    monitor()
