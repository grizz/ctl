import os


def output():
    path = os.path.dirname(__file__)
    path = os.path.join(path, "data", "ctl_pypi_test.txt")
    with open(path, "r") as fh:
        print((fh.read()))


if __name__ == "__main__":
    output()
