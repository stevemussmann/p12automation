import pandas
import warnings

from natsort import natsort_keygen

class Progeny():
	'Class for manipulating Progeny output into pandas dataframe'

	def __init__(self, fn):
		self.fn = fn #input filename
	
	def toPandas(self):
		warnings.simplefilter(action='ignore', category=pandas.errors.PerformanceWarning) #performance warning stfu

		# read file into pandas dataframe
		df = pandas.read_csv(self.fn, sep='\t', header=0, index_col=1)
		df = df.rename(columns=lambda x: x.strip()) # strip whitespace from column names
		df.sort_index(axis=1, inplace=True, key=lambda col: col.str.lower() ) # sort columns by lower case equivalent of names
		df.sort_index(axis=0, inplace=True, key=natsort_keygen() ) # sort rows by sample name

		# move 'Pedigree' back to the first column
		first_column = df.pop('Pedigree')
		df.insert(0, 'Pedigree', first_column)

		# probably need to strip columns with sex data
		remove = ['Pedigree','zOts_SexID_GHpsi-348-A1','zOts_SexID_GHpsi-348-A2']
		sexMarkers = pandas.concat([df.pop(x) for x in remove], axis=1)

		# replace nan values with ?
		df.fillna("?",inplace=True)

		return df, sexMarkers
