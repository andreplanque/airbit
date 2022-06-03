import numpy as np
import matplotlib.pyplot as plt


class Measurement:  # Class for storing data from a measurement
    def __init__(self, x, y, x_label=..., y_label=..., title=...):
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
             loc: str = "upper right"):  # Plot the data
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

    def __repr__(self):  # Representation of the object
        return f"{self.title}\n{self.x_label} = {self.x}\n{self.y_label} = {self.y}"


class Airbit:
    def __init__(self, data, offset):
        self._data = data.T
        self.time = [(n * 5) / (60 * 24) + offset for n in range(len(self._data[0]))]  # Time in days
        self.PM10 = Measurement(self.time, map(float, self._data[3]), 'Tid [d]', 'PM10 [µg/m³]', 'PM10')
        self.PM25 = Measurement(self.time, map(float, self._data[4]), 'Tid [d]', 'PM2.5 [µg/m³]', 'PM2.5')
        self.hum = Measurement(self.time, map(float, self._data[5]), 'Tid [d]', 'Luftfuktighet [%]', 'Luftfuktighet')
        self.temp = Measurement(self.time, map(float, self._data[6]), 'Tid [d]', 'Temperatur [°C]', 'Temperatur')

    @classmethod
    def from_file(cls, data_file_name: str, offset: float = 0.5):
        with open(data_file_name, 'r') as f:
            data = np.loadtxt(f, dtype=str, delimiter=',')
        return cls(data, offset)


def main():
    pm10_anb = Measurement([0.5, 7.5], [20, 20], title="PM10 Årsverdi")
    pm25_anb = Measurement([0.5, 7.5], [10, 10], title="PM2.5 Årsverdi")
    pm10_anb2 = Measurement([0.5, 7.5], [50, 50], title="PM10 Døgnverdi")
    airbit = Airbit.from_file('LESNING.CSV')
    # pm25_anb.plot(legend=True)
    # pm10_anb2.plot(legend=True)
    # plt.show()


if __name__ == '__main__':
    main()
