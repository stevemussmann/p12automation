# p12automation

## Installation
Most of the below (i.e., Conda installation, creation of folders, modification of .bashrc, etc.) only needs to be done once for setup of this package unless you move to a new computer.

### Conda Installation

```
conda create -n p12Automation -c conda-forge -c bioconda -c r r=4.2 python=3 pandas rpy2 openpyxl natsort r-tidyverse r-jsonlite r-devtools gfortran
```

Activate the conda environment you just created
```
conda activate p12Automation
```

Once installed, open R from the command line and install rubias

```
install.packages("rubias", dependencies=TRUE, repos='http://cran.rstudio.com/')
```

Download the related package and install from Bash
```
wget https://github.com/timothyfrasier/related/raw/master/related_1.0.tar.gz
R CMD INSTALL related_1.0.tar.gz
```

### Python code setup

Make a set of folders for local installation
```
mkdir -p $HOME/local/scripts/python
mkdir -p $HOME/local/bin
```

Modify your .bashrc file to point to the 'bin' folder you just made
```
echo "export PATH=$PATH:$HOME/local/bin" >> $HOME/.bashrc
```

Exit all open terminal windows and open a new one. Then change directories to the python folder you created. Download this github repository, then move into the directory and make sure the p12auto.py script is executable.
```
cd $HOME/local/scripts/python
git clone https://github.com/stevemussmann/p12automation.git
cd $HOME/local/scripts/python/p12automation
chmod u+x p12auto.py
```

Link against the p12auto.py script in your $HOME/local/bin folder
```
cd $HOME/local/bin
ln -s $HOME/local/scripts/python/p12automation/p12auto.py
```

(Recommended) Modify line 22 of `$HOME/local/scripts/python/p12automation/comline.py` to provide the default location of the R functions for rubias. If you don't do this modification then you will need to specify the path to rubiasCode.R every time you run this program. If you followed the instructions above, you should be able to just change out my user name (mussmann) for yours in the line of code shown below:

```
default="/home/mussmann/local/scripts/python/p12automation/rubiasCode.R",
```

## Running p12auto.py

Before running the code, you must first activate the conda environment you created:
```
conda activate p12Automation
```

You can then run the code with the following command. 
* Replace 'int' with the sequential event number for the current rapid response year. 
* Replace the paths in the command below with the paths to your progeny output text file, and the baseline genotype data in rubias format:
```
p12auto.py -e int -f /path/to/progeny/output -b /path/to/baseline
```

## Outputs

The program produces four output files:
* **P12_CHRR_Event_\<int\>_\<year\>Genotypes_and_Results.txt**: This is the primary results file. The first sheet contains fully formatted output ready to be added to the FAX sheet. The remaining four sheets contain rubias output that has been formatted to match data summaries from the program oncor.
* **P12_CHRR_Event_<int>_<year>.mixture.rubias.txt**: Sample genotypes formatted for input to rubias. This is the genotype file that was processed by the p12auto.py pipeline.
* **P12_CHRR_Event_<int>_<year>.genepop.txt**: Sample genotypes in genepop format. 
* **P12_CHRR_Event_<int>_<year>.json**: Rubias results in JSON format. This file was produced only to facilitate transfer of rubias results from R back to Python for data processing. This file can be ignored.
