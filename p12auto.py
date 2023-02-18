#!/usr/bin/env python

from comline import ComLine
from genepop import Genepop
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
	df = pandas.read_csv(input.args.infile, sep='\t', header=0, index_col=1)
	df = df.rename(columns=lambda x: x.strip()) # strip whitespace from column names
	print(df)
	df.sort_index(axis=1, inplace=True, key=lambda col: col.str.lower() ) # sort columns by lower case equivalent of names
	df.sort_index(axis=0, inplace=True, key=natsort_keygen() ) # sort rows by sample name

	# move 'Pedigree' back to the first column
	first_column = df.pop('Pedigree')
	df.insert(0, 'Pedigree', first_column)
	df.to_csv("testfile.csv")

	# probably need to strip columns with sex data
	remove = ['Pedigree','zOts_SexID_GHpsi-348-A1','zOts_SexID_GHpsi-348-A2']
	sexMarkers = pandas.concat([df.pop(x) for x in remove], axis=1)
	print(sexMarkers)

	# replace nan values with ?
	df.fillna("?",inplace=True)
			
	# convert input file to genepop format
	gp = Genepop(df)
	loclist = gp.convert()
	gp.writeGenepop()

	# convert to rubias format
	rb = Rubias(df, loclist)
	rubiasMixture = rb.writeRubias()

	# run rubias
	rbdf = rb.runRubias(input.args.baseline, rubiasMixture)
	#newdf = rbdf.groupby('indiv').apply(lambda df_: df_[['collection','z_score']].values.flatten()).apply(pandas.Series).reset_index()
	newdf = rbdf.pivot(index='indiv', columns='collection', values='PofZ').sort_index(axis=0, key=natsort_keygen())

	# custom sort the dataframe so columns are in consistent order
	sortOrder={"sortOrder":{"FRHsp":0,"BUTsp":1,"MILsp":2,"DERsp":3,"FRHfl":4,"MILfl":5,"DERfl":6,"MOKfl":7,"BATfl":8,"SAClf":9,"SACwin":10}}
	df_dict = pandas.DataFrame.from_dict(sortOrder, orient='index')
	print(df_dict)
	newdf = pandas.concat([newdf, df_dict]).sort_values(by="sortOrder", axis=1)
	newdf.drop(labels="sortOrder", axis=0, inplace=True)

	print(rbdf)
	print(newdf)

main()

raise SystemExit
