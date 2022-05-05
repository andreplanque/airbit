import numpy as np


class Airbit:
    def __init__(self, data_file: str):
        with open(data_file, 'r') as f:
            data = np.loadtxt(f, delimiter=',')
        self.data = data


def main():
    airbit = Airbit('data.csv')
    print(airbit.data)


if __name__ == '__main__':
    main()