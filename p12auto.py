#!/usr/bin/env python

from comline import ComLine
from genepop import Genepop
from progeny import Progeny
from rubias import Rubias
from natsort import natsort_keygen

import argparse
import os
import pandas
import sys

def main():
	print("Automating p12!")

	input = ComLine(sys.argv[1:])

	# read file into pandas dataframe
	prog = Progeny(input.args.infile)
	df, sexData = prog.toPandas()

	print(sexData)
			
	# convert input file to genepop format
	gp = Genepop(df)
	loclist = gp.convert()
	gp.writeGenepop()

	# convert to rubias format
	rb = Rubias(df, loclist)
	rubiasMixture = rb.writeRubias()

	# run rubias
	rb.runRubias(input.args.baseline, rubiasMixture, input.args.pathtorcode)

	# parse rubias output
	rb.parseRubiasOutput()
	rb.compileRubiasResults(sexData)
	rb.writeExcel()

main()

raise SystemExit
