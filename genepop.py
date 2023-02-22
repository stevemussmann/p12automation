import pandas
import collections

class Genepop():
	'Class for converting pandas dataframe to Genepop format'

	def __init__(self, df, currEvent):
		self.pdf = df #pandas dataframe derived from progeny output
		self.nucleotides = {'A':'101', 'C':'102', 'G':'103', 'T':'104', '-':'105', '?':'000'} #nucleotide map for conversion
		self.locuslist = list() #maintains list of loci for genepop header
		self.d = collections.defaultdict(dict) # dictionary to hold converted data for genepop format
		self.ce = currEvent

	def convert(self):
		print("Writing genepop file: ", self.ce, ".genepop.txt.", sep="")
		print("")
		for index, row in self.pdf.iterrows():
			for name, allele in row.items():
				name = name.replace("-SWFSC96", "")
				if name.endswith("-A1"):
					name = name.replace("-A1", "")
					if name not in self.locuslist:
						self.locuslist.append(name) # add to list of loci
					self.d[index][name] = self.nucleotides[allele]
				elif name.endswith("-A2"):
					name = name.replace("-A2", "")
					self.d[index][name] = self.d[index][name] + self.nucleotides[allele]
		return self.locuslist # return the list of loci for use in rubias converter

	def writeGenepop(self):
		fn = self.ce + ".genepop.txt"
		fh = open(fn, 'w')
		fh.write(self.ce)
		fh.write("\n")
		for loc in self.locuslist:
			fh.write(loc)
			fh.write("\n")
		fh.write("POP")
		fh.write("\n")
		for sample in self.d.keys():
			fh.write(sample)
			fh.write(" ,")
			for locus in self.d[sample].keys():
				fh.write(" ")
				fh.write(self.d[sample][locus])
			fh.write("\n")
		fh.close()
