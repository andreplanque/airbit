import numpy as np


class Airbit:
    def __init__(self, data_file_name: str):
        with open(data_file_name, 'r') as f:
            data = np.loadtxt(f, dtype=str, delimiter=',')
        self.data = data.T
        self.time = self.data[0]
        self.time_from_start = self.time_to_seconds_from_start()
        self.PM10 = list(map(float, self.data[3]))
        self.PM25 = list(map(float, self.data[4]))
        self.hum = list(map(float, self.data[5]))
        self.temp = list(map(float, self.data[6]))

    @staticmethod
    def seconds_from_start_of_year(time: str):
        time = time.split('-')
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days_in_month[1] += 1 if not int(time[0]) % 4 else 0
        days_to_month = sum(days_in_month[:int(time[1]) - 1]) * 24 * 3600
        t = list(map(int, time[2].replace('T', ':').split(':')))
        return t[0] * 3600 * 24 + t[1] * 3600 + t[2] * 60 + t[3] + days_to_month

    def time_to_seconds_from_start(self):
        seconds_from_start_of_year = [self.seconds_from_start_of_year(t) for t in self.time]
        seconds_from_start = [s - seconds_from_start_of_year[0] for s in seconds_from_start_of_year]
        return seconds_from_start


def main():
    airbit = Airbit('data.csv')
    print(airbit.time_from_start)
    print(airbit.PM10)
    print(airbit.PM25)
    print(airbit.hum)
    print(airbit.temp)


if __name__ == '__main__':
    main()
