import numpy as np
import matplotlib.pyplot as plt


class Measurement:
    def __init__(self, x, y, x_label: str = ..., y_label: str = ..., title: str = ...):
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


# TODO: add time of day (rush hour etc) and day of week
class Airbit:
    def __init__(self):
        self._data: np.ndarray = ...
        self._start_time: str = ...
        self.time: np.ndarray = ...
        self.PM10: Measurement = ...
        self.PM25: Measurement = ...
        self.hum: Measurement = ...
        self.temp: Measurement = ...

    def from_file(self, data_file_name: str, start_time: str = ...):
        with open(data_file_name, 'r') as f:
            _data = np.loadtxt(f, dtype=str, delimiter=',')
        self._data = _data.T
        self._start_time = start_time
        self.time = [n * 5 * 60 for n in range(len(self._data[0]))]
        self.PM10 = Measurement(self.time, map(float, self._data[3]), 'Time [s]', 'PM10 [µg/m³]', 'PM10')
        self.PM25 = Measurement(self.time, map(float, self._data[4]), 'Time [s]', 'PM25 [µg/m³]', 'PM25')
        self.hum = Measurement(self.time, map(float, self._data[5]), 'Time [s]', 'Humidity [%]', 'Humidity')
        self.temp = Measurement(self.time, map(float, self._data[6]), 'Time [s]', 'Temperature [°C]', 'Temperature')


def main():
    airbit = Airbit()
    airbit.from_file('data.csv',)
    airbit.PM10.plot(show=True, label=True)


if __name__ == '__main__':
    main()
