import pandas
import collections

from natsort import natsort_keygen
from rpy2.robjects.packages import STAP

class Rubias():
	'Class for functions pertaining to Rubias'

	def __init__(self, df, loclist):
		self.pdf = df #pandas dataframe derived from progeny output
		self.nucleotides = {'A':'1', 'C':'2', 'G':'3', 'T':'4', '-':'5', '?':''} #nucleotide map for conversion
		self.locuslist = loclist # locuslist output from genepop file converter
		self.rbdf = pandas.DataFrame() # dataframe that will hold raw rubias output

	def writeRubias(self):
		print("writing to rubias format")
		filename = "Event.mixture.rubias.txt"
		fh = open(filename, 'w')

		# write header line
		fh.write("sample_type\trepunit\tcollection\tindiv")
		for loc in self.locuslist:
			fh.write("\t")
			fh.write(loc)
			fh.write("\t")
			allele2 = loc + ".1"
			fh.write(allele2)
		fh.write("\n")

		# write data lines
		for index, row in self.pdf.iterrows():
			fh.write("mixture\t\tUNK\t") # UPDATE THIS - grab from 'Pedigree' column of original pandas data frame
			fh.write(index)
			for name, allele in row.items():
				fh.write("\t")
				fh.write(self.nucleotides[allele])
			fh.write("\n")
		fh.close()

		return filename

	def runRubias(self, base, mix, ptrc):
		print("running rubias")

		# read in rubias functions
		try:
			with open(ptrc, 'r') as f:
				string = f.read()
			self.rfunc = STAP(string, 'rbfunc')
		except FileNotFoundError as e:
			print("")
			print("File containing R functions was not found:")
			print(ptrc)
			print(e)
			print("Did you specify the correct path and/or file name with the '-r' option?")
			print("")
			raise SystemExit
			

		try:
			self.rfunc.runRubias(b=base, m=mix, j="outfile.json") #UPDATE - make json output file name customizable
		except rpy2.rinterface_lib.embedded.RRuntimeError as e:
			print("")
			print("Error in funRubias R function:")
			print(e)
			print("")
			raise SystemExit

		self.rbdf = pandas.read_json("outfile.json")

	def parseRubiasOutput(self):
		
		newdf = self.rbdf.pivot(index='indiv', columns='collection', values='PofZ').sort_index(axis=0, key=natsort_keygen())

		# custom sort the dataframe so columns are in consistent order
		sortOrder={"sortOrder":{"FRHsp":0,"BUTsp":1,"MILsp":2,"DERsp":3,"FRHfl":4,"MILfl":5,"DERfl":6,"MOKfl":7,"BATfl":8,"SAClf":9,"SACwin":10}}
		df_dict = pandas.DataFrame.from_dict(sortOrder, orient='index')
		print(df_dict)
		newdf = pandas.concat([newdf, df_dict]).sort_values(by="sortOrder", axis=1)
		newdf.drop(labels="sortOrder", axis=0, inplace=True)

		print(self.rbdf)
		print(newdf)

