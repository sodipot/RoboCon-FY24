import spidev
import time

class Gyro:
    def __init__(cs_pin=1):
        # set max SCLK freq. to 5MHz
        pass

    def write_bytes(self, address, value):
        return self.spi.xfer2([0x00 | address, value])

    def read_bytes(self, address, n=1):
        return self.spi.xfer2([0x80 | address] + [0x00 for _ in range(n)])

    def set_up(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,1)
        self.spi.max_speed_hz = 500000
        self.fs_sel = 0         # default:0, min-max: 0-7

    def get_gyro_sensitivity(self) -> int:
        if (self.fs_sel == 0):
            return 16.4
        elif (self.fs_sel == 1):
            return 32.8
        elif (self.fs_sel == 2):
            return 65.5
        elif (self.fs_sel == 3):
            return 131
        elif (self.fs_sel == 4):
            return 262
        elif (self.fs_sel == 5):
            return 524.3
        elif (self.fs_sel == 6):
            return 1048.6
        elif (self.fs_sel == 7):
            return 2097.2


    def twos_complement_to_signed_int(self, value: int) -> int:
        """2の補数表現の2バイト値を符号付き整数に変換する"""
        if value & 0x8000:  # 最上位ビットが1か確認
            return value - 0x10000
        return value

    def signed_int_to_twos_complement(self, value: int) -> int:
        return (value)

    def start(self):
        self.write_bytes(0x4e, 0x0f)

    def stop(self):
        self.write_bytes(0x4e, 0x00)
        self.spi.close()

    def calibration(self, data_count=30):
        temp_offset_wz = 0.0
        sensitivity = self.get_gyro_sensitivity()

        for i in range(1,data_count):
            # read out
            temp_offset_wz = temp_offset_wz + self.get_true_wz(sensitivity)

            time.sleep(0.02)

        offset_wz = temp_offset_wz / data_count

        if offset_wz > 64:
            offset_wz = 64
        elif offset_wz < -64:
            offset_wz = -64

        offset_value = int(offset_wz / 0.03125)

        offset_msb = offset_value >> 8
        offset_lsb = offset_value & 0xFF

        print(offset_value)

        self.write_bytes(0x7a, offset_lsb)
        self.write_bytes(0x7a, offset_msb)


    def get_true_wz(self, sensitivity=16.4):
        [_, raw_wz1, raw_wz0] = self.read_bytes(0x29, 2)
        wz = self.twos_complement_to_signed_int((raw_wz1 << 8) | raw_wz0) / sensitivity

        return wz

    def get_raw_wz(self):
        [_, raw_wz1, raw_wz0] = self.read_bytes(0x29, 2)
        raw_wz = (raw_wz1 << 8) | raw_wz0
        return raw_wz







if __name__ == "__main__":
    my_gyro = Gyro()
    my_gyro.set_up()
    time.sleep(0.5)
    my_gyro.start()
    time.sleep(0.5)

    sensitivity = my_gyro.get_gyro_sensitivity()

    time.sleep(0.1)
    for _ in range (1,20):
        print(my_gyro.get_true_wz(sensitivity))
        time.sleep(0.10)

    my_gyro.calibration(data_count=100)

    time.sleep(0.1)

    for _ in range (1,20):
        print(my_gyro.get_true_wz(sensitivity))
        time.sleep(0.10)


    my_gyro.stop()


