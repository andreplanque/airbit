import numpy as np
import matplotlib.pyplot as plt


class Measurement:
    def __init__(self, x, y, x_label: str | None = ..., y_label: str | None = ..., title: str | None = ...):
        self.x = list(x)
        self.y = list(y)
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

    def plot(self, *,
             show: bool = False,
             save: bool = False,
             label: bool = False,
             legend: bool = False,
             loc: str = "upper left"):
        if label and self.x_label is not None and self.y_label is not None:
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)
            plt.title(self.title)
        if legend:
            plt.legend(loc=loc)
            plt.plot(self.x, self.y, label=self.title)
        else:
            plt.plot(self.x, self.y)
        if show:
            plt.show()
        elif save:
            plt.savefig(self.title.lower() + ".eps")

    def __repr__(self):
        return f"{self.title}\n{self.x_label} = {self.x}\n{self.y_label} = {self.y}"


class Airbit:
    def __init__(self):
        self._data: np.ndarray = ...
        self._time: np.ndarray = ...
        self.time: np.ndarray = ...
        self.PM10: Measurement = ...
        self.PM25: Measurement = ...
        self.hum: Measurement = ...
        self.temp: Measurement = ...

    def from_file(self, data_file_name: str, no_time: bool = False):
        with open(data_file_name, 'r') as f:
            _data = np.loadtxt(f, dtype=str, delimiter=',')
        self._data = _data.T
        self._time = self._data[0]
        if no_time:
            self.time = [n * 5 * 60 for n in range(len(self._time))]
        else:
            self.time = self._time_to_seconds_from_start()
        self.PM10 = Measurement(self.time, map(float, self._data[3]), 'Time [s]', 'PM10 [µg/m³]', 'PM10')
        self.PM25 = Measurement(self.time, map(float, self._data[4]), 'Time [s]', 'PM25 [µg/m³]', 'PM25')
        self.hum = Measurement(self.time, map(float, self._data[5]), 'Time [s]', 'Humidity [%]', 'Humidity')
        self.temp = Measurement(self.time, map(float, self._data[6]), 'Time [s]', 'Temperature [°C]', 'Temperature')

    @staticmethod
    def _seconds_from_start_of_year(time: str):
        time = time.split('-')
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days_in_month[1] += 1 if not int(time[0]) % 4 else 0
        days_to_month = sum(days_in_month[:int(time[1]) - 1]) * 24 * 3600
        t = list(map(int, time[2].replace('T', ':').split(':')))
        return (t[0] - 1) * 3600 * 24 + t[1] * 3600 + t[2] * 60 + t[3] + days_to_month

    def _time_to_seconds_from_start(self):
        seconds_from_start_of_year = [self._seconds_from_start_of_year(t) for t in self._time]
        seconds_from_start = [s - seconds_from_start_of_year[0] for s in seconds_from_start_of_year]
        return seconds_from_start


def main():
    airbit = Airbit()
    airbit.from_file('data.csv', no_time=True)
    airbit.PM10.plot(show=True, label=True)


if __name__ == '__main__':
    main()
