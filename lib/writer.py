import logging


class Writer:
    @staticmethod
    def init() -> None:
        f = open("CHANGELOG", "w")
        f.close()

    @staticmethod
    def writeDiff(diff: str):
        try:
            f = open("CHANGELOG", "a")
            f.write(diff)
            f.flush()
        except IOError as e:
            logging.error("I/O error({0}): {1}".format(e.errno, e.strerror))
