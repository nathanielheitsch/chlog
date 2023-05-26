import logging


class Writer:
    def __init__(self) -> None:
        self.f = open("CHANGELOG", "w")
        self.f.close()

    def writeDiff(self, diff: str):
        try:
            self.f = open("CHANGELOG", "a")
            self.f.write(diff)
            self.f.flush()
        except IOError as e:
            logging.error("I/O error({0}): {1}".format(e.errno, e.strerror))
