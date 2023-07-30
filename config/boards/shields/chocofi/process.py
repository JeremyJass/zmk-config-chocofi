import re


MAP_GAP = 2
SPLIT_GAP = 5
MAX_COLS = 10
LEFT_PADDING = 3

# ALIGN = "centered"
ALIGN = "left"


class ZMKConfigParser:

    def __init__(self, keymap_file):
        self.layer_names = []
        self.layer_bindings = []

        layer_index = 0
        keymap_block_found = False
        compatible_found = False
        in_bindings = False

        with open(keymap_file, "r") as f:
            for l in f.readlines():

                if not keymap_block_found:
                    m = re.search("keymap", l)
                    if (m):
                        keymap_block_found = True
                elif not compatible_found:
                    m = re.search("compatible", l)
                    if (m):
                        compatible_found = True
                elif not in_bindings:
                    m = re.search("{", l)
                    if (m):
                        self.layer_names.append(l.strip(' {\n'))
                    else:
                        m = re.search("bindings", l)
                        if (m):
                            in_bindings = True
                            self.layer_bindings.append([])
                else:
                    m = re.search(">;", l)
                    if (m):
                        in_bindings = False
                        layer_index += 1
                    else:
                        records = l.split("&")
                        records = ["&"+r.strip() for r in records[1:]]
                        self.layer_bindings[layer_index].append(records)
        self.longest_string = self.longest_string()


    def longest_string(self):
        longest_string = 0
        for layer in self.layer_bindings:
            for row in layer:
                for record in row:
                    if (len(record) > longest_string):
                        longest_string = len(record)
        return longest_string


    def get_spaces(self, num):
        spaces = ""
        for i in range(int(num)):
            spaces += " "
        return spaces


    def output(self):
        for layer in self.layer_bindings:
            row_string = ""
            for row in layer:
                col_id = 0
                row_string += self.get_spaces(LEFT_PADDING)
                if (len(row) < MAX_COLS):
                    offset = int((MAX_COLS - len(row)) / 2)
                    row_string += self.get_spaces(offset * (self.longest_string + MAP_GAP))
                    col_id += offset
                for record in row:
                    col_id += 1
                    tpad = (self.longest_string + MAP_GAP) - len(record)
                    lpad = 0

                    if (ALIGN == "centered"):
                        if ((tpad % 2) != 0):
                            lpad += 1
                            tpad -= 1
                        rpad = tpad / 2
                        lpad += rpad
                    elif (ALIGN == "left"):
                        rpad = tpad

                    if (col_id == (MAX_COLS / 2)):
                        rpad += SPLIT_GAP
                    row_string += self.get_spaces(lpad) + record + self.get_spaces(rpad)
                row_string = row_string.rstrip() + "\n"
            print(row_string)


if __name__ == '__main__':

    zmk = ZMKConfigParser("chocofi.keymap")

    zmk.output()

    print("done")