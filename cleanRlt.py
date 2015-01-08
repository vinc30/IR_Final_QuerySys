"""
Usage:
    python cleanRlt.py `Result file with notation` `output name`
"""


import sys
from os.path import exists


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Error: Invalid input arguments"
    assert exists(sys.argv[1]), "Error: Input file " + sys.argv[1] + " is missing "
    assert not exists(sys.argv[2]), "Error: Output file already exists"
    fin = open(sys.argv[1], "r")
    fout = open(sys.argv[2], "w")
    for i, line in enumerate(fin):
        fout.write(str(i + 1) + "\n")
        fout.write(line.strip().replace("[", "").replace("]", "").replace(",", "") + "\n")
    fin.close()
    fout.close()
