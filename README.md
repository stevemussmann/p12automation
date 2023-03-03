# p12automation

## Table of Contents
1. [Installation](#installation)
    * [Installing and Configuring Miniconda](#condainstall)
    * [Making a Conda Environment](#condaenv)
    * [Setting Up the Python Code](#python)
    * [Make a Folder for Input Files](#quickruns)
2. [Running the Program](#running)
3. [Program Outputs](#outputs)

<hr>

## Installation <a name="installation"></a>
Most of the below (i.e., Conda installation, creation of folders, modification of .bashrc, etc.) only needs to be done once for setup of this package unless you move to a new computer.

### Conda Installation <a name="condainstall"></a>
Miniconda needs to be installed if it is not already configured on your computer. If you already have Miniconda installed, skip to "Making a Conda Environment"

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
Once again, exit and relaunch WSL before proceeding. 

<hr>

### Making a Conda Environment <a name="condaenv"></a>
Run the following command to create the p12Automation conda environment:
```
conda create -n p12Automation -c conda-forge -c bioconda -c r r=4.2 python=3 pandas rpy2 openpyxl natsort r-tidyverse r-jsonlite r-devtools r-demerelate gfortran
```

Activate the conda environment you just created
```
conda activate p12Automation
```

A conda package does not exist for rubias, so it was not included when you created the conda environment. Install it with this command:
```
R --slave -e "install.packages('rubias', dependencies=TRUE, repos='http://cran.rstudio.com')"
```

<hr>

### Python code setup <a name="python"></a>

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

Modify line 33 of `$HOME/local/scripts/python/p12automation/comline.py` to provide the default location of the R functions for rubias. If you don't do this modification then you will need to specify the path to `rubiasCode.R` every time you run this program. The following sed command should automatically accomplish this task:

```
sed -i "s/mussmann/$USER/g" $HOME/local/scripts/python/p12automation/comline.py
```

<hr>

### Make a Folder for Input Files <a name="quickruns"></a>

If you are using Windows Subsystem for Linux, then it can be cumbersome to constantly switch back and forth from Windows to WSL. I recommend making a folder on the desktop where you can run this program, and linking it in Linux.

Step 1: On your Windows Desktop, create a folder titled 'p12runs' where you will put files for processing with the p12auto.py pipeline.

Step 2: Link this folder in your home directory under WSL:
```
cd ~/
WINDOWSUSER=`powershell.exe '$env:UserName' | sed 's/\r//g'`
ln -s /mnt/c/Users/$WINDOWSUSER/Desktop/p12runs
```
You should now have a link within your home directory under WSL that provides a shortcut to the 'p12runs' folder you made on your Windows desktop. When you place files in this folder on your Windows desktop, they should be visible within `/home/$USER/p12runs` from WSL. 

<hr>

## Running p12auto.py <a name="running"></a>

Step 1: Before running the code, you must first open WSL and activate the conda environment you created:
```
conda activate p12Automation
```

Step 2: In Windows, put your input files into the 'p12runs' folder on your Desktop. In WSL, change directories into your 'p12runs' folder:
```
cd ~/p12runs
```

Step 3: You can then run the code with the following command. 
* Replace 'int' with the sequential event number for the current rapid response year. 
* Replace the paths in the command below with the paths to your progeny output text file, and the baseline genotype data in rubias format. The 'progeny' file should be the text file output from progeny that has 'Pedigree' as the first column heading
```
p12auto.py -e int -f /path/to/progeny/output -b /path/to/baseline
```

The full list of command line options from the `--help` menu is below. 
```
usage: p12auto.py [-h] -b BASELINE -e EVNUM -f INFILE [-m MINLOCI] [-r PATHTORCODE] [-w]

options:
  -h, --help            show this help message and exit
  -b BASELINE, --baseline BASELINE
                        Specify the path to the baseline (required).
  -e EVNUM, --evnum EVNUM
                        Specify the rapid response event number for your current year (required).
  -f INFILE, --infile INFILE
                        Specify the text file output from Progeny (required).
  -m MINLOCI, --minloci MINLOCI
                        Provide the minimum number of loci required to report an assignment. Default = 80 loci (optional).
  -r PATHTORCODE, --pathtorcode PATHTORCODE
                        Provide the path to the R functions for rubias (optional.
  -w, --nowarn          Supresses R console warnings. Invoke this option to stop supression of R console warnings (optional).
```

<hr>

## Outputs <a name="outputs"></a>

The program produces four output files. In the file names, \<int\> represents the sequential rapid response number (-e input to p12auto.py) and \<year\> represents the current rapid response year:
* **P12_CHRR_Event_\<int\>_\<year\>Genotypes_and_Results.txt**: This is the primary results file. The first sheet contains fully formatted output ready to be added to the FAX sheet. The remaining four sheets contain rubias output that has been formatted to match data summaries from the program oncor.
* **P12_CHRR_Event_\<int\>_\<year\>.mixture.rubias.txt**: Sample genotypes formatted for input to rubias. This is the genotype file that was processed by the p12auto.py pipeline.
* **P12_CHRR_Event_\<int\>_\<year\>.genepop.txt**: Sample genotypes in genepop format. 
* **P12_CHRR_Event_\<int\>_\<year\>.json**: Rubias results in JSON format. This file was produced only to facilitate transfer of rubias results from R back to Python for data processing. This file can be ignored.
