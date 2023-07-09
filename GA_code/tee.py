class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, text):
        for file in self.files:
            file.write(text)
            file.flush()  # Ensure immediate write

    def flush(self):
        for file in self.files:
            file.flush()