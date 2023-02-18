import argparse
import os.path

class ComLine():
	'Class for implementing command line options'


	def __init__(self, args):
		parser = argparse.ArgumentParser()
		parser._action_groups.pop()
		required = parser.add_argument_group('required arguments')
		optional = parser.add_argument_group('optional arguments')
		required.add_argument("-f", "--infile",
							dest='infile',
							required=True,
							help="Specify the text file output from Progeny."
		)
		required.add_argument("-b", "--baseline",
							dest='baseline',
							required=True,
							help="Specify the path to the baseline."
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
