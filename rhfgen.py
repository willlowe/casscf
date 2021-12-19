#!/usr/local/bin/python

import pdb
import sys, os
import string

inputfile = sys.argv[1]


class File():
    def __init__(self, number):
        self.filenumber = number
        self.filepath = str(self.filenumber) + "_rhf.inp"

        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        else:
            pass

        with open(self.filepath, 'x+') as newfile:
            newfile.write(
                " $BASIS GBASIS=ccd $END\n"
                " $CONTRL SCFTYP=RHF RUNTYP=ENERGY ISPHER=1 $END\n"
                " $NBO $END\n $SYSTEM MWORDS=512 MEMDDI=128 $END\n"
                "\n"
                " $DATA\n"
            )

    def close(self):
        with open(self.filepath, 'a') as newfile:
            newfile.write(" $END")

    def append(self, data):
        with open(self.filepath, 'a') as newfile:
            newfile.write(data)


if __name__ == '__main__':
    with open(inputfile) as file:
        lines = file.readlines()
        masterfilepath = inputfile + "_fixed"

        if os.path.exists(masterfilepath):
            os.remove(masterfilepath)
        else:
            pass

        with open(masterfilepath, 'a') as newfile:
            for line in lines:
                newfile.write(
                    line.replace(" H", " H 1")
                        .replace(" C", " C 6")
                        .replace(" N", " N 7")
                        .replace(" O", " O 8")
                        .replace(" B", " B 5"))

    with open(masterfilepath) as file:
        lines = file.readlines()

    i = 0
    newsubfile = File(i)
    for line in lines:
        if line[0].isdigit() and i > 0:
            newsubfile.close()
            newsubfile = File(i)
            i = i + 1
        elif line[0].isdigit():
            newsubfile = File(i)
            i = i + 1

        if line[0] == 'F':
            newsubfile.append("C1\n")
        else:
            newsubfile.append(line)
    else:
        newsubfile.close()
