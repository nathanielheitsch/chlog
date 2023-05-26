class Writer:
    def __init__(self) -> None:
        pass
        # self.f = open("CHANGELOG", "w")
        # self.f.close()

    def writeDiff(self, diff: str):
        self.f = open("CHANGELOG", "a")
        self.f.write(diff)
        self.f.close()
