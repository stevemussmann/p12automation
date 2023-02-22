import collections
import datetime
import pandas

from natsort import natsort_keygen
from rpy2.robjects.packages import STAP

class Rubias():
	'Class for functions pertaining to Rubias'

	def __init__(self, df, loclist, currEvent):
		self.pdf = df #pandas dataframe derived from progeny output
		self.nucleotides = {'A':'1', 'C':'2', 'G':'3', 'T':'4', '-':'5', '?':''} #nucleotide map for conversion
		self.locuslist = loclist # locuslist output from genepop file converter
		self.rbdf = pandas.DataFrame() # dataframe that will hold raw rubias output
		self.ce = currEvent

		# dataframes for reporting
		self.dfByPop = pandas.DataFrame()
		self.dfByRepGroup = pandas.DataFrame()
		self.dfPrBaseline = pandas.DataFrame()
		self.dfPrRepGroup = pandas.DataFrame()
		self.lociScored = pandas.DataFrame()
		self.printedResults = pandas.DataFrame()

	def writeRubias(self):
		fn = self.ce + ".mixture.rubias.txt"
		print("Writing in rubias format to ", fn, ".", sep="")
		fh = open(fn, 'w')

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

		return fn

	def runRubias(self, base, mix, ptrc):
		print("Running rubias...")

		# make file name for json file
		fn = self.ce + ".json"

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
			self.rfunc.runRubias(b=base, m=mix, j=fn)
		except rpy2.rinterface_lib.embedded.RRuntimeError as e:
			print("")
			print("Error in funRubias R function:")
			print(e)
			print("")
			raise SystemExit

		try:
			self.rbdf = pandas.read_json(fn)
		except FileNotFoundError as e:
			print("")
			print("JSON file that was supposed to be produced by R code was not found:")
			print(e)
			print("")
			raise SystemExit
			

	def parseRubiasOutput(self):
		
		# extract required data from rubias output and organize into more sensible dataframe
		self.dfPrBaseline = self.rbdf.pivot(index='indiv', columns='collection', values='PofZ').sort_index(axis=0, key=natsort_keygen())

		# get number of loci scored as reported by rubias
		self.lociScored = self.rbdf[['indiv','n_non_miss_loci']].copy()
		self.lociScored.drop_duplicates(inplace=True) # must drop duplicates before reindexing. Otherwise there will be many non-unique indexes.
		self.lociScored.set_index('indiv', inplace=True)

		# create nested dictionary that will be temporarily added to dataframe for soring so that columns are in consistent order
		sortOrder={"sortOrder":{"FRHsp":0,"BUTsp":1,"MILsp":2,"DERsp":3,"FRHfl":4,"MILfl":5,"DERfl":6,"MOKfl":7,"BATfl":8,"SAClf":9,"SACwin":10}}
		df_dict = pandas.DataFrame.from_dict(sortOrder, orient='index') # convert sortOrder to pandas dataframe

		# declare lists of reporting unit groups
		fall=["FRHfl","MILfl","DERfl","MOKfl","BATfl","SAClf"]
		spring=["FRHsp","BUTsp","MILsp","DERsp"]
		winter=["SACwin"]

		self.dfPrBaseline = pandas.concat([self.dfPrBaseline, df_dict]).sort_values(by="sortOrder", axis=1)
		self.dfPrBaseline.drop(labels="sortOrder", axis=0, inplace=True)

		# declare pandas dataframe to hold reporting unit probabilities
		self.dfPrRepGroup = pandas.DataFrame()

		# sum probabilities for spring, fall, and winter runs
		self.dfPrRepGroup['Fall'] = self.dfPrBaseline[fall].sum(axis=1)
		self.dfPrRepGroup['Spring'] = self.dfPrBaseline[spring].sum(axis=1)
		self.dfPrRepGroup['Winter'] = self.dfPrBaseline[winter].sum(axis=1)

		# make dataframe and populate it with top reporting unit for each sample
		self.dfByRepGroup = pandas.DataFrame()
		self.dfByRepGroup['Best Estimate'] = self.dfPrRepGroup.idxmax(axis=1)
		self.dfByRepGroup['Probability'] = self.dfPrRepGroup.max(axis=1)

		# make dataframe and populate it with top three gsi matches for each sample
		# for this one I need to specify columns and data type,
		# otherwise it does weird things with NaN values since I skip low probability results
		self.dfByPop = pandas.DataFrame()
		new_cols = ['Best Estimate', 'Best Probability', '2nd Best Estimate', '2nd Probability', '3rd Best Estimate', '3rd Probability']
		self.dfByPop = self.dfByPop.reindex(self.dfByPop.columns.union(new_cols), axis=1)
		convert_dict = {'Best Estimate': str,
						'Best Probability': float,
						'2nd Best Estimate': str,
						'2nd Probability': float,
						'3rd Best Estimate': str,
						'3rd Probability': float
		}
		self.dfByPop=self.dfByPop.astype(convert_dict)

		# get top three results
		for ind,line in self.dfPrBaseline.iterrows():
			results=line.nlargest(n=3)
			count=0 # counter to put results into first, second, third columns
			for run,prob in results.items():
				count=count+1 #increase counter
				if count==1:
					self.dfByPop.at[ind,'Best Estimate'] = run
					self.dfByPop.at[ind,'Best Probability'] = prob
				elif count==2:
					if prob < 0.01:
						self.dfByPop.at[ind,'2nd Best Estimate'] = pandas.NA
						self.dfByPop.at[ind,'2nd Probability'] = pandas.NA
					else:
						self.dfByPop.at[ind,'2nd Best Estimate'] = run
						self.dfByPop.at[ind,'2nd Probability'] = prob
				elif count==3:
					if prob < 0.01:
						self.dfByPop.at[ind,'3rd Best Estimate'] = pandas.NA
						self.dfByPop.at[ind,'3rd Probability'] = pandas.NA
					else:
						self.dfByPop.at[ind,'3rd Best Estimate'] = run
						self.dfByPop.at[ind,'3rd Probability'] = prob
				else:
					print("This code should be unreachable. How did you get here?")

	def compileRubiasResults(self, dfSex):
		print("Compiling rubias results...")
		print("")

		# get date for entering into excel sheet
		today = datetime.date.today()
		yesterday = today - datetime.timedelta(days = 1)
		tdy = today.strftime("%-m-%-d-%-y")
		ydy = yesterday.strftime("%-m-%-d-%-y")

		# get current time for reporting
		now = datetime.datetime.now()
		ct = now.strftime("%I:%M %p").lower()

		# format dates and times
		sent = tdy + " @ " + ct
		received = ydy + " @ 10:30 am"

		# add dates received and results sent
		self.printedResults = pandas.DataFrame(index=self.dfByRepGroup.index)
		self.printedResults['Date/Time Received R1-CGL'] = received
		self.printedResults['Date LSNFH Hatchery Notified'] = sent

		# add sex to dataframe
		self.printedResults['Sex'] = dfSex['zOts_SexID_GHpsi-348-A2'].map({'Y':'Male','X':'Female','?':'No Call'})

		# add pop to dataframe
		self.printedResults['Rubias Pop'] = self.dfByRepGroup['Best Estimate']
		self.printedResults['Rubias Probability'] = self.dfByRepGroup['Probability'].round(4)

		# add genetic call
		self.printedResults['Genetic Call'] = self.dfByRepGroup['Best Estimate'].map({'Winter':'WR','Fall':'Non-WR','Spring':'Non-WR'}, na_action='ignore')

		# add number of loci scored
		self.printedResults['Number of Loci Scored'] = self.lociScored['n_non_miss_loci']

		for index, val in self.printedResults['Number of Loci Scored'].items():
			if self.printedResults.at[index, 'Sex'] != "No Call":
				self.printedResults.at[index, 'Number of Loci Scored'] = str(int(val)+1) + " out of 96"
			else:
				self.printedResults.at[index, 'Number of Loci Scored'] = str(val) + " out of 96"

	def writeExcel(self):
		fn = self.ce + "Genotypes_and_Results.xlsx"
		print("Writing final output to excel file: ", fn, ".", sep="")
		with pandas.ExcelWriter(fn) as writer:
			self.printedResults.to_excel(writer, sheet_name='Results')
			self.dfByPop.to_excel(writer, sheet_name='Rubias Result by Pop', float_format="%.4f")
			self.dfByRepGroup.to_excel(writer, sheet_name='Rubias Result by Rep Group', float_format="%.4f")
			self.dfPrBaseline.to_excel(writer, sheet_name='Rubias Pr(Baseline Pop)', float_format="%.4f")
			self.dfPrRepGroup.to_excel(writer, sheet_name='Rubias Pr(Rep Group)', float_format="%.4f")
