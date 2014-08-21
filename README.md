leb-clustering
==============

Clustering and analysis software for the Laboratory of Experimental Biophysics, EPFL

Contents
+ main.m - The script used for reading in data and creating figures.
+ process_data.m - Primary function for clustering localization data and computing cluster statistics.
+ data_mining.m - Helper script for investigating new data; use before processing all the data with main.m.
+ second_central_moment.m - A rewrite of Matlab's var function to better handle array data.
+ dbscan.m - DBSCAN implementation in Matlab. Originally written by Michal Daszykowski at the University of Silesia.