library(rubias)
library(tidyverse)
library(jsonlite)

runRubias <- function( b, m, j ){
	# read input files
	baseline <- read.csv(b, sep="\t")
	mixture <- read.csv(m, sep="\t")

	# apply proper data type (integer) to all SNP columns. This is necessary in
	# cases where a column is missing SNP data for all individuals
	# mostly needed to be done to mixture but also good practice to do for baseline
	baseline[,-c(1:5)]<-sapply(baseline[,-c(1:5)], as.integer)
	mixture[,-c(1:5)]<-sapply(mixture[,-c(1:5)], as.integer)

	# run rubias
	mix_est <- infer_mixture(reference=baseline, mixture=mixture, gen_start_col=5, reps = 20000, burn_in = 10000)

	# also might be able to write to json file and read into python for parsing?
	x <- toJSON(mix_est$indiv_posteriors, pretty=TRUE)
	writeLines(x, j)
}
