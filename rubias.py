import pandas
import collections

from rpy2.robjects.packages import STAP

class Rubias():
	'Class for functions pertaining to Rubias'

	def __init__(self, df, loclist):
		self.pdf = df #pandas dataframe derived from progeny output
		self.nucleotides = {'A':'1', 'C':'2', 'G':'3', 'T':'4', '-':'5', '?':''} #nucleotide map for conversion
		self.locuslist = loclist # locuslist output from genepop file converter
		self.rubiasCode = "rubiasCode.R"

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

	def runRubias(self, base, mix):
		print("running rubias")

		# read in rubias functions
		with open(self.rubiasCode, 'r') as f:
			string = f.read()
		self.rfunc = STAP(string, 'rbfunc')

		try:
			self.rfunc.runRubias(b=base, m=mix, j="outfile.json") #UPDATE - make json output file name customizable
		except rpy2.rinterface_lib.embedded.RRuntimeError:
			print("Error in funRubias R function.")

		df = pandas.read_json("outfile.json")

		return df

