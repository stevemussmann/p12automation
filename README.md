# p12automation

## Conda Installation

```
conda create -n p12Automation -c conda-forge -c bioconda -c r r=4.2 python=3 pandas rpy2 openpyxl natsort r-tidyverse r-jsonlite r-devtools gfortran
```

Activate the conda environment you just created
```
conda activate p12Automation
```

Once installed, open R from the command line and install rubias

```
install.packages("rubias", dependencies=TRUE)
```

Download the related package and install from Bash
```
wget https://github.com/timothyfrasier/related/raw/master/related_1.0.tar.gz
R CMD INSTALL related_1.0.tar.gz
```
