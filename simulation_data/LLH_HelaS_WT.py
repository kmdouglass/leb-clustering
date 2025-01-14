"""Compute the log-likelihood for the wildtype Hela S telomeres.

"""

__author__ = 'Kyle M. Douglass'
__email__  = 'kyle.douglass@epfl.ch'

from numpy import save
from STORMlikeChains import STORMlikeChains_helpers as Helpers

import os
os.chdir('..')

experimentDatasetName = os.getcwd() + '/saved_distrs/Original_Data_S_dataset_RgTrans'

# List of NumPyDB database names without the file suffix.
#dbNames = [os.getcwd() + '/simulation_data/simData_HeLaS_WT_2015-8-21']
dbNames = [os.getcwd() + '/simulation_data/simData_HeLaS_WT_2015-10-8']

#outputFName = os.getcwd() + '/simulation_data/llh_Original_Data_S_dataset_RgTrans2015-8-21.npy'
outputFName = os.getcwd() + '/simulation_data/llh_Original_Data_S_dataset_RgTrans2015-10-8.npy'

# Compute the log-likelihood for each simulated distribution.
llh = Helpers.computeLLH(dbNames, experimentDatasetName)

# Save the log-likelihood data to a .npy file.
with open(outputFName, mode = 'wb') as fileOut:
    save(fileOut, llh)
