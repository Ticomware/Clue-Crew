INDICATOR_CHARACTER = "|"

class FileParser:
    def __init__(self, file_path):
        self.line_index = 0
        with open(file_path) as file:
            self.lines = [line for line in file.readlines() if len(line.strip()) != 0]

    def get_line_indicator(self):
        if not self.is_end_of_file():
            indicator = self.lines[self.line_index].split(INDICATOR_CHARACTER)[0].strip()
        else:
            indicator = ""
        return indicator

    def parse_line(self):
        if not self.is_end_of_file():
            content = self.lines[self.line_index].split(INDICATOR_CHARACTER)[1].strip()
        else:
            content = ""
        self.line_index += 1
        return content

    def is_end_of_file(self):
        return self.line_index > (len(self.lines) - 1)