# p12automation

## Installation
Most of the below (i.e., Conda installation, creation of folders, modification of .bashrc, etc.) only needs to be done once for setup of this package unless you move to a new computer.

### Conda Installation

Launch Windows Subsystem for Linux (WSL) and download the miniconda installer:
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Install miniconda accepting all defaults. Answer 'yes' when asked if you want to initialize conda. 

```
bash https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Exit and relaunch WSL before proceeding. When your terminal window reopens, run the following command.

```
conda config --set auto_activate_base false
```

Once again, exit and relaunch WSL before proceeding. Then run the following command to create the p12Automation conda environment:
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

### Python code setup

Make a set of folders for local installation
```
mkdir -p $HOME/local/scripts/python
mkdir -p $HOME/local/bin
```

Modify your .bashrc file to point to the 'bin' folder you just made
```
echo 'export PATH=$PATH:$HOME/local/bin' >> $HOME/.bashrc
```

Exit all open terminal windows and open a new one. The code below 1) changes directories to the python folder you created 2) Downloads this github repository, 3) moves into the directory, and 4) makes sure the p12auto.py script is executable. If you get a 'server certificate verification failed' error, see the next paragraph below.

```
cd $HOME/local/scripts/python
git clone https://github.com/stevemussmann/p12automation.git
cd $HOME/local/scripts/python/p12automation
chmod u+x p12auto.py
```

If you received the error `server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none` then run the following command: `git config --global http.sslverify false`. Now rerun the above code block starting from the `git clone https://github.com/stevemussmann/p12automation.git` command before proceeding.

Link against the p12auto.py script in your $HOME/local/bin folder
```
cd $HOME/local/bin
ln -s $HOME/local/scripts/python/p12automation/p12auto.py
```

(Recommended) Modify line 33 of `$HOME/local/scripts/python/p12automation/comline.py` to provide the default location of the R functions for rubias. If you don't do this modification then you will need to specify the path to rubiasCode.R every time you run this program. Run the following sed command, replacing `yourusernamehere` with your linux username.

```
cd $HOME/local/scripts/python/p12automation/
sed -i 's/mussmann/yourusernamehere/g'
```

If you don't feel comfortable running the sed command, then you can open the comline.py file in a text editor and change out my user name (mussmann) for yours in line 33 of code, which should be as shown below:

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

The full list of command line options from the `--help` menu is below. Commands in the 'usage' line surrounded by brackets [] are optional:
```
usage: p12auto.py [-h] -b BASELINE -e EVNUM -f INFILE [-m MINLOCI] [-r PATHTORCODE] [-w]

options:
  -h, --help            show this help message and exit
  -b BASELINE, --baseline BASELINE
                        Specify the path to the baseline.
  -e EVNUM, --evnum EVNUM
                        Specify the rapid response event number for your current year.
  -f INFILE, --infile INFILE
                        Specify the text file output from Progeny.
  -m MINLOCI, --minloci MINLOCI
                        Provide the minimum number of loci required to report an assignment. Default = 80 loci.
  -r PATHTORCODE, --pathtorcode PATHTORCODE
                        Provide the path to the R functions for rubias.
  -w, --nowarn          Supresses R console warnings. Invoke this option to stop supression of R console warnings.
```

## Outputs

The program produces four output files. In the file names, \<int\> represents the sequential rapid response number (-e input to p12auto.py) and \<year\> represents the current rapid response year:
* **P12_CHRR_Event_\<int\>_\<year\>Genotypes_and_Results.txt**: This is the primary results file. The first sheet contains fully formatted output ready to be added to the FAX sheet. The remaining four sheets contain rubias output that has been formatted to match data summaries from the program oncor.
* **P12_CHRR_Event_\<int\>_\<year\>.mixture.rubias.txt**: Sample genotypes formatted for input to rubias. This is the genotype file that was processed by the p12auto.py pipeline.
* **P12_CHRR_Event_\<int\>_\<year\>.genepop.txt**: Sample genotypes in genepop format. 
* **P12_CHRR_Event_\<int\>_\<year\>.json**: Rubias results in JSON format. This file was produced only to facilitate transfer of rubias results from R back to Python for data processing. This file can be ignored.
