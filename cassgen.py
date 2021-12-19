#!/usr/local/bin/python

import pdb
import sys, os
from sys import argv
from rhfgen import File

masterfilepath = sys.argv[1]


class CassFile(File):
    def __init__(self, number, no, aso, ase, nce, n, sai, dat):
        super().__init__(number)
        self.filenumber = number
        self.datfile = dat
        self.filepath = str(self.filenumber) + "_casscf.inp"

        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        else:
            pass

        # get ordering line from reorderings correpsonding to file name
        try:
            with open('reorderings.txt') as reodering:
                lines = reodering.readlines()
        except FileNotFoundError:
            print("reordering file not found")
            exit()

        try:
            reorderingline = lines[number]
            print(reorderingline)
        except IndexError:
            print("line does not exsist, will print line not found")
            reorderingline = "line not found"


        try:
            with open(self.filepath, 'x+') as newfile:
                newfile.write(
                    " $CONTRL SCFTYP=MCSCF ICHARG=0 MULT=1\n"
                    "  ISPHER=1 $END\n"
                    " $GUESS GUESS=MOREAD NORB=" + no + " NORDER=1\n"
                    "  "  + reorderingline +""
                    " $BASIS gbasis=ccd $END\n"
                    " $MCSCF MAXIT=200 focas=.T. CISTEP=ALDET $END\n"
                    " $SYSTEM MWORDS=128 $END\n"
                    " $DET NACT=" + aso + " NELS=" + ase + " NCORE=" + nce + " $END\n"
                    " $DET NSTATE=" + n + " $END\n"
                    " $DET WSTATE(1)=" + sai + " $END\n"
                    " $CIINP CASTRF=.T. $END\n"
                    " $STATPT PROJCT=.F. $END\n"
                    " $DATA\n"
                )
        except FileExistsError:
            print("file already exists")

    def close(self):
        with open(self.filepath, 'a') as newfile:
            newfile.write(" $END\n")
            try:
                if self.datfile == "empty":
                    with open(str(self.filenumber) + "_rhf.dat", 'r') as datfile:
                        datlines=datfile.readlines()
                else:
                    with open(self.datfile + str(self.filenumber) + "_rhf.dat", 'r') as datfile:
                        datlines=datfile.readlines()

            except FileNotFoundError:
                print("dat file not found, appending error message")
                datlines=["could not find dat file"]
            for line in datlines:
                newfile.write(line)
            newfile.write("\n $END")


def newsubfilegen(i):
    return CassFile(i, no=args['-no'][0], aso=args['-aso'][0], ase=args['-ase'][0], nce=args['-nce'][0],
                    n=args['-n'][0], sai=args['-sai'][0], dat=args['-dat'][0])


if __name__ == '__main__':
    args = {}
    currentkey = 'ignore'
    currentvalues = []

    for i in argv:
        if i[0] == '-':
            currentvalues = []
            currentkey = i
        else:
            currentvalues.append(i)
            args[currentkey] = currentvalues

    del args['ignore']

    print(args)

    with open(masterfilepath) as file:
        lines = file.readlines()

    i = 0

    newsubfile = newsubfilegen(i)
    for line in lines:
        if line[0].isdigit() and i > 0:
            newsubfile.close()
            newsubfile = newsubfilegen(i)
            i = i + 1
        elif line[0].isdigit():
            newsubfile = newsubfilegen(i)
            i = i + 1

        if line[0] == 'F':
            newsubfile.append("C1\n")
        else:
            newsubfile.append(line)
    else:
        newsubfile.close()
