import argparse
import os.path

class ComLine():
	'Class for implementing command line options'


	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser.add_argument("-f", "--infile",
							dest='infile',
							required=True,
							help="Specify the text file output from Progeny."
		)
		parser.add_argument("-b", "--baseline",
							dest='baseline',
							required=True,
							help="Specify the path to the baseline."
		)
		parser.add_argument("-r", "--pathtorcode",
							dest='pathtorcode',
							default="/home/mussmann/local/scripts/python/p12automation/rubiasCode.R",
							help="Provide the path to the R functions for rubias."
		)

		self.args = parser.parse_args()

		#check if files exist
		self.exists( self.args.infile )
		self.exists( self.args.baseline )

	def exists(self, filename):
		if( os.path.isfile(filename) != True ):
			print("")
			print(filename, "does not exist")
			print("Exiting program...")
			print("")
			raise SystemExit
