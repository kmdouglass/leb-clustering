leb-clustering
==============

Clustering and analysis software for the Laboratory of Experimental
Biophysics, EPFL

This code automatically filters and analyzes the localization data
from the Telomere/STORM experiments and saves the analyzed size
distributions to text files. These distributions can then be used for
plotting or for further analyses, such as doing maximum likelihood
estimations.

## Contents ##
### Files ###
+ **data_mining.m** - Helper script for investigating new data; use
  for exploring the datasets before processing all the data with
  main.m.
+ **data_visualization_main.m** - Runs all the different visualization
  scripts for the various experiments. It also generates an HTML
  report for each experiment.
+ **dbscan.m** - DBSCAN implementation in Matlab. Originally written
  by Michal Daszykowski at the University of Silesia.
+ **dbscan_sweep_params.m** Performs a parameter sweep of the DBSCAN
  input parameters to find the best set of inputs. (_Warning_: this
  can take a long time to run.)
+ **Makefile** - Used to automatically run the various scripts in the
  correct order for analyzing the localization data and saving the
  results.
+ **process\_helper.m** - The script used for reading in raw
  localization data, setting filtering properties, and sending the
  data to the *process\_data.m* script. *process\_data.m* does the
  actual filtering and computation of the radius of gyration and other
  calculations.
+ **process_data.m** - Primary function for clustering localization
  data and computing cluster statistics.
+ **README.md** - This help file
+ **saveDistFiles.m** - Used to save the distribution data to text
  files.

### Folders ###
+ **analyses** - Contains filtered and clustered data for all the
  experiments, including scripts for automatically generating
  plots. (These are named *data_visualization.m* and are found in each
  sub-directory for the important experiments.)
+ **data_structres** - Matlab files defining where to find the raw
  localization data for each experiment.
+ **figures** - Figures that are generated by scripts for visualizing
  the processed data.
+ **misc** - Mostly old, miscellaneous files. Includes some analyses
  of the Southern blots.
+ **org** - Notes kept in org-mode.
+ **private** - Folder containing all the helper functions used for
  data visualization and processing. The name _private_ is a special
  name for folders in Matlab. It designates where functions used in
  scripts located in the directory above _private_ are held.
+ **reports\_and\_meetings** - Various reports and presentations from
  the project.
+ **saved_distrs** - Folder containing the distributions of the
  statistics computed from the clustered localizations. Currently,
  this is only the radius of gyration data.
+ **simulation_data** - Numpy files and pickled Python databases
  containing the simulated radius of gyration data for generating the
  parameter space plots.
+ **writeup** - Miscellaneous files for the writeup.

## Instructions ##

If anything is not clear from this README for how to run the analyses,
you can either look at the Makefile in the project root directory or
send an e-mail to <mailto:kyle.douglass@epfl.ch>.

### Running the entire analysis ###

The entire analyses can be run simply by navigating to the root
directory (which contains the process\_helper.m and process\_data.m
scripts) and typing

	make

Note that this currently requires that localization data are stored in
a certain directory on the external harddrive on Kyle's office
computer. This is planned to change soon.

It is also assumed that you are using GNU Make on a Linux-based
system. It may be possible to use GNU Make to assemble this analysis
on a Windows system, but this has not been tested.

### Running only selected localization analyses
Individual analyses may be run by doing one of two steps:

1. Use the *process\_helper.m* and *process\_data.m* scripts to
   generate .mat files containing the processed localizations.
2. Use the Makefile in the _analyses/_ folder with an argument
   corresponding to a certain experiment to process. For example,

```
	cd analyses
	make experiment0
```

   generates the Matlab .mat file for experiment number 0, which
   studied the wild type Hela cells. The *cd analyses* command is not
   necessary if you're already inside the analyses folder.

   Note that running an individual analysis this way _will not_
   generate updated distribution text files or run the
   data_visualization scripts for the experiment. To do this, you must
   go back to the project's root directory and type

```
	make saveData
	make dataVis
```

### Performing the likelihood calculations ###

Computing the likelihood values from simulated distributions requires
the following:

1. The PolymerPy Python package developed in the LEB
2. Simulated datasets; these will have .dat and .map suffixes and are
   stored in the *simulated_data* directory. The filenames will have
   a date and a brief description of what was simulated. The two
   primary simulation datasets in this analysis are
   *rw\_2015-1-26\_HelaL\_WT* and *rw\_2015-2-2\_HelaS\_WT*.
3. Measured datasets; these are in the *saved_distrs* directory. The
   two most important files for this analysis are
   *Original\_Data\_L\_dataset\_RgTrans* and
   *Original\_Data\_S\_dataset\_RgTrans*.

To compute the likelihood values, type

```sh
	make calcLLH
```

This will generate numpy (.npy) files containing the likelihood values
that the measured datasets were generated by any of the simulated
datasets. The likelihood data is stored in the *simulation\_data* and
is prefixed with *llh*, which stands for log-likelihood.

### Generate the publication figures ###

Once all the other steps have been run, you can generate the figures
for the publication by typing

```sh
	make pubPlots
```

The output from this step will indicate which figures have been
generated. They are normally stored in the directory
*figures/output_figs*.

## Software Versions ##

The following software packages were used to perform this
analysis. This list is not meant to serve as a dependency list, but
instead as documentation for the versions of software used.

### Matlab

+ Matlab R2014a (8.3.0.532) 64-bit

### Linux tools

+ Make (3.81-8.2) 64-bit

### Python

Python 3.4.1 was used for this project, though in general any Python3
interpretor with the proper packages installed should work.

The following Python packages were installed in a virtualenv. The long
line from github is the PolymerPy package that was developed in the
LEB for inferring polymer properties from super-resolution datasets.

```sh
(PolymerPy)douglass@lebpc18:~/Telomeres$ pip freeze
matplotlib==1.4.3
nose==1.3.4
numpy==1.9.2
-e git+https://github.com/kmdouglass/PolymerPy@56dd01b19fef417c39429034285faf91119c9b15#egg=PolymerPy-master
pyparsing==2.0.3
python-dateutil==2.4.1
pytz==2015.2
scikit-learn==0.15.2
scipy==0.15.1
six==1.9.0
wheel==0.24.0
```
