#!/usr/bin/env python

from comline import ComLine
from genepop import Genepop
from progeny import Progeny
from rubias import Rubias
from natsort import natsort_keygen

import argparse
import datetime
import os
import pandas
import sys

def main():
    # read command line input
	input = ComLine(sys.argv[1:])

	#construct event name
	today = datetime.date.today()
	year = today.year
	currEvent="P12_CHRR_Event_" + str(input.args.evnum).zfill(2) + "_" + str(year)
	print("Running event ", currEvent, ".", sep="")

	# read file into pandas dataframe
	prog = Progeny(input.args.infile)
	df, sexData = prog.toPandas()

	# convert input file to genepop format
	gp = Genepop(df, currEvent)
	loclist = gp.convert()
	gp.writeGenepop()

	# convert to rubias format
	rb = Rubias(df, loclist, currEvent)
	rubiasMixture = rb.writeRubias()

	# run rubias
	rb.runRubias(input.args.baseline, rubiasMixture, input.args.pathtorcode)

	# parse rubias output
	rb.parseRubiasOutput()
	rb.compileRubiasResults(sexData)
	rb.writeExcel()

main()

raise SystemExit
