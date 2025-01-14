"""Script for generating the publication quality parameter-space plots
for the telomere manuscript.

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rcParams
from STORMlikeChains.STORMlikeChains_helpers import unpackLLH, loadModel
from option_d import test_cm as myCMap # Custom Parula-like colormap

# Set global matplotlib settings
journalFontSize = 6
figureSize = (1.75, 1.57)

fontpath = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
prop = font_manager.FontProperties(fname = fontpath)
rcParams['font.family'] = prop.get_name()
rcParams.update({'font.size'       : journalFontSize,
                 'legend.fontsize' : journalFontSize,
                 'axes.titlesize'  : journalFontSize,
                 'figure.figsize'  : figureSize,
                 'figure.dpi'      : 600,
                 'figure.edgecolor' : (1,1,1,0),
                 'figure.facecolor' : (1,1,1,0),
                 'figure.subplot.bottom' : 0.125,
                 'axes.linewidth' : 0.5})


"""The following was originally and mostly written in an IPython
notebook, so the formatting reflects this style.

"""

results = {'Hela L' : {'LLH' : None,
                       'packRatio' : None,
                       'pLength' : None},
           'Hela S' : {'LLH' : None,
                       'packRatio' : None,
                       'pLength' : None}}

### Read in the log-likelihood data

# In[2]:

# Read in Hela L
currDataset = '../simulation_data/llh_Original_Data_L_dataset_RgTrans2015-8-19.npy'

with open(currDataset, mode = 'rb') as inFile:
    hl = np.load(inFile)

# Unpack the dataset
results['Hela L']['packRatio']   = hl['f0']
results['Hela L']['pLength']     = hl['f1']
(CL, LPL, results['Hela L']['LLH']) = unpackLLH(hl)


# In[3]:

# Read in Hela S
currDataset = '../simulation_data/llh_Original_Data_S_dataset_RgTrans2015-8-21.npy'

with open(currDataset, mode = 'rb') as inFile:
    hs = np.load(inFile)

# Unpack the dataset
results['Hela S']['packRatio']   = hs['f0']
results['Hela S']['pLength']     = hs['f1']
(CS, LPS, results['Hela S']['LLH']) = unpackLLH(hs)

### Setup plots for the parameter space close to the mean

# The log-likelihood gives us a relative measure of the similarity
# between the measured distribution and the simulated one. However,
# higher log-likelihood values may not necessarily correspond to
# better simulated distributions. We should also consider looking at
# all simulated distributions with means that are a certain distance
# from the experimental mean, say +/- 5 nm. This is a very rough
# estimate of the day-to-day variation in the mean values of the
# distributions.

# In[6]:

from scipy.stats import sem

# Experimental distributions
LExpDist = np.loadtxt('../saved_distrs/Original_Data_L_dataset_RgTrans')
SExpDist = np.loadtxt('../saved_distrs/Original_Data_S_dataset_RgTrans')

LMean = np.mean(LExpDist)
SMean = np.mean(SExpDist)

LSEM = sem(LExpDist)
SSEM = sem(SExpDist)

# Model distributions
LModelDists = loadModel(['../simulation_data/simData_HeLaL_WT_2015-8-19'])
SModelDists = loadModel(['../simulation_data/simData_HeLaS_WT_2015-8-21'])

LModelMeans = {k: np.mean(v[1]) for k, v in LModelDists.items()}
SModelMeans = {k: np.mean(v[1]) for k, v in SModelDists.items()}


# In[7]:

# Set the +/- amount around the experimental mean for filtering out
# incorrect parameter space values
err = 5

# Filter out datasets with means far from the experimental mean
LMeansFiltered = {k: v for k, v in LModelMeans.items() if np.abs(LMean - v) < err}
SMeansFiltered = {k: v for k, v in SModelMeans.items() if np.abs(SMean - v) < err}

# Convert the filtered parameter space values into arrays for plotting
LGoodParams = list(LMeansFiltered.keys())
SGoodParams = list(SMeansFiltered.keys())


### Make distribution plots for the paper

##### Hela L

# In[8]:

c  = [35, 55,  30, 80]
lp = [40, 100, 80, 90]

myBins = np.arange(10, 250, 5)

fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, sharex = True, sharey = True)

ax1.hist(LExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax1.hist(LModelDists[(c[0],lp[0])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         normed = True)
ax1.text(20, 0.021, r'c = %i, $\ell_p$ = %i' % (c[0], lp[0]))
ax1.set_ylim((0, 0.025))
ax1.tick_params(axis = 'y', which = 'major', pad = 1.5)
plt.yticks([0.000, 0.0125, 0.025])

ax2.hist(LExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax2.hist(LModelDists[(c[1],lp[1])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         normed = True)
ax2.text(20, 0.021, r'c = %i, $\ell_p$ = %i' % (c[1], lp[1]))
ax2.set_ylim((0, 0.025))

ax3.hist(LExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax3.hist(LModelDists[(c[2],lp[2])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         normed = True)
ax3.text(20, 0.021, r'c = %i, $\ell_p$ = %i' % (c[2], lp[2]))
ax3.tick_params(axis = 'y', which = 'major', pad = 1.5)
ax3.set_ylim((0, 0.025))
ax3.set_xticklabels([0, 50, 100, 150, 200, 250], rotation = 45)
ax3.tick_params(axis = 'x', which = 'major', pad = 0.6)

plt.yticks([0.000, 0.0125, 0.025])

ax4.hist(LExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax4.hist(LModelDists[(c[3],lp[3])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         label = 'Simulation',
         normed = True)
ax4.text(20, 0.021, r'c = %i, $\ell_p$ = %i' % (c[3], lp[3]))
ax4.set_ylim((0, 0.025))
ax4.set_xticklabels([0, 50, 100, 150, 200, 250], rotation = 45)
ax4.tick_params(axis = 'x', which = 'major', pad = 0.6)

fig.text(0.525, 0.027, 'Radius of gyration, nm', ha='center', va='center')
fig.text(0.025, 0.5, 'Probability density', ha='center', va='center', rotation='vertical')

ax1.spines['top'].set_visible(False);   ax1.xaxis.set_ticks_position('bottom')
ax1.spines['right'].set_visible(False); ax1.yaxis.set_ticks_position('left')
ax2.spines['top'].set_visible(False);   ax2.xaxis.set_ticks_position('bottom') 
ax2.spines['right'].set_visible(False); ax2.yaxis.set_ticks_position('left')
ax3.spines['top'].set_visible(False);   ax3.xaxis.set_ticks_position('bottom') 
ax3.spines['right'].set_visible(False); ax3.yaxis.set_ticks_position('left')
ax4.spines['top'].set_visible(False);   ax4.xaxis.set_ticks_position('bottom') 
ax4.spines['right'].set_visible(False); ax4.yaxis.set_ticks_position('left')

ax1.spines['bottom'].set_linewidth(0.5); ax1.spines['left'].set_linewidth(0.5)
ax2.spines['bottom'].set_linewidth(0.5); ax2.spines['left'].set_linewidth(0.5)
ax3.spines['bottom'].set_linewidth(0.5); ax3.spines['left'].set_linewidth(0.5)
ax4.spines['bottom'].set_linewidth(0.5); ax4.spines['left'].set_linewidth(0.5)

# Place legend above subplots
leg = plt.legend(bbox_to_anchor=(0.75, 1.02),
                 bbox_transform=plt.gcf().transFigure)
leg.draw_frame(False)

# Squeeze subplots into a smaller bounding box, relative to the figure
plt.tight_layout(w_pad = 0.5, rect = [0, 0, 1, 0.9])
plt.savefig('output_figs/HelaL_param_space_dists.svg')
plt.savefig('output_figs/HelaL_param_space_dists.pdf')
plt.savefig('output_figs/HelaL_param_space_dists.png')

# Plot the parameter space

# In[9]:

packRatio, pLength = zip(*LGoodParams)

options = {'vmin'   : -1.6e4,
           'vmax'   : -8000,
           'origin' : 'lower',
           'extent' : [results['Hela L']['packRatio'].min(), results['Hela L']['packRatio'].max(),
                       results['Hela L']['pLength'].min(),   results['Hela L']['pLength'].max()],
           'aspect' : 'auto'}

fig = plt.figure()

# Log-likelihood map
ax1 = fig.add_axes([0.13, 0.11, 0.84, 0.76])
llhMap = ax1.imshow(results['Hela L']['LLH'], cmap = myCMap, **options)
ax1.set_xticks([10, 30, 50, 70, 90])
ax1.tick_params(axis='x', which='major', pad=0.7)
ax1.tick_params(axis='y', which='major', pad=1.5)

#plt.tight_layout(pad=0)

## Plot simulated points
#props = {'alpha' : 0.6,
#         'edgecolors' : None}
#plt.scatter(packRatio, 
#            pLength,
#            s = 10,
#            c = 'white',
#            **props)

# Plot points from distributions
props = {'marker' : '^'}
plt.scatter(c, lp, s = 25, c = 'red', **props)

# Plot contours
levels = [-1.25e4, -1.15e4, -1.05e4, -0.95e4, -0.85e4]
colors = [(0.2, 0.2, 0.2),
          (0.4, 0.4, 0.4),
          (0.6, 0.6, 0.6),
          (0.8, 0.8, 0.8),
          (1.0, 1.0, 1.0)]
plt.contour(CL, LPL, results['Hela L']['LLH'], levels, colors = colors, linewidths = 0.5)

#plt.xlim((results['Hela L']['packRatio'].min(), results['Hela L']['packRatio'].max()))
plt.xlim((results['Hela L']['packRatio'].min(), 90))
plt.ylim((results['Hela L']['pLength'].min(),   200))
plt.xlabel('Packing density, bp/nm', labelpad = 0.5)
plt.ylabel('Persistence length, nm', labelpad = -1)

cbaxes = fig.add_axes([0.13, 0.9, 0.84, 0.05]) 
cbar = plt.colorbar(llhMap, cax = cbaxes, ticks = [-16000, -14000, -12000, -10000, -8000], orientation = 'horizontal')
cbar.ax.xaxis.set_ticklabels(['', '', '', '', ''])
cbar.ax.xaxis.set_ticks_position('top')

plt.savefig('output_figs/HelaL_param_space.svg')
plt.savefig('output_figs/HelaL_param_space.pdf')
plt.savefig('output_figs/HelaL_param_space.png')


##### Hela S

# In[10]:

c  = [20, 25, 20, 50]
lp = [40, 60, 80, 90]

myBins = np.arange(10, 200, 5)

fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, sharex = True, sharey = True)

ax1.hist(SExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax1.hist(SModelDists[(c[0],lp[0])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         normed = True)
ax1.text(20, 0.043, r'c = %i, $\ell_p$ = %i' % (c[0], lp[0]))
ax1.set_ylim((0, 0.05))
ax1.tick_params(axis = 'y', which = 'major', pad = 1.5)
plt.yticks([0.00, 0.025, 0.05])

ax2.hist(SExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax2.hist(SModelDists[(c[1],lp[1])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         normed = True)
ax2.text(20, 0.043, r'c = %i, $\ell_p$ = %i' % (c[1], lp[1]))
ax2.set_ylim((0, 0.05))

ax3.hist(SExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax3.hist(SModelDists[(c[2],lp[2])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         normed = True)
ax3.text(20, 0.043, r'c = %i, $\ell_p$ = %i' % (c[2], lp[2]))
ax3.tick_params(axis = 'y', which = 'major', pad = 1.5)
ax3.set_ylim((0, 0.025))
ax3.set_xticklabels([0, 50, 100, 150, 200], rotation = 45)
ax3.tick_params(axis = 'x', which = 'major', pad = 0.6)

plt.yticks([0, 0.025, 0.050])

ax4.hist(SExpDist,
         bins = myBins,
         histtype = 'step',
         color = '#000000',
         alpha = 0.5,
         label = 'Experiment',
         normed = True)
ax4.hist(SModelDists[(c[3],lp[3])][1],
         bins = myBins,
         histtype = 'step',
         color = '#333333',
         label = 'Simulation',
         normed = True)
ax4.text(20, 0.043, r'c = %i, $\ell_p$ = %i' % (c[3], lp[3]))
ax4.set_ylim((0, 0.025))
ax4.set_xticklabels([0, 50, 100, 150, 200], rotation = 45)
ax4.tick_params(axis = 'x', which = 'major', pad = 0.6)

ax1.set_ylim((0, 0.05))
ax2.set_ylim((0, 0.05))
ax3.set_ylim((0, 0.05))
ax4.set_ylim((0, 0.05))

fig.text(0.525, 0.027, 'Radius of gyration, nm', ha='center', va='center')
fig.text(0.025, 0.5, 'Probability density', ha='center', va='center', rotation='vertical')

ax1.spines['top'].set_visible(False);   ax1.xaxis.set_ticks_position('bottom')
ax1.spines['right'].set_visible(False); ax1.yaxis.set_ticks_position('left')
ax2.spines['top'].set_visible(False);   ax2.xaxis.set_ticks_position('bottom') 
ax2.spines['right'].set_visible(False); ax2.yaxis.set_ticks_position('left')
ax3.spines['top'].set_visible(False);   ax3.xaxis.set_ticks_position('bottom') 
ax3.spines['right'].set_visible(False); ax3.yaxis.set_ticks_position('left')
ax4.spines['top'].set_visible(False);   ax4.xaxis.set_ticks_position('bottom') 
ax4.spines['right'].set_visible(False); ax4.yaxis.set_ticks_position('left')

ax1.spines['bottom'].set_linewidth(0.5); ax1.spines['left'].set_linewidth(0.5)
ax2.spines['bottom'].set_linewidth(0.5); ax2.spines['left'].set_linewidth(0.5)
ax3.spines['bottom'].set_linewidth(0.5); ax3.spines['left'].set_linewidth(0.5)
ax4.spines['bottom'].set_linewidth(0.5); ax4.spines['left'].set_linewidth(0.5)

# Place legend above subplots
leg = plt.legend(bbox_to_anchor=(0.75, 1.02),
                 bbox_transform=plt.gcf().transFigure)
leg.draw_frame(False)

# Squeeze subplots into a smaller bounding box, relative to the figure
plt.tight_layout(w_pad = 0.5, rect = [0, 0, 1, 0.9])
plt.savefig('output_figs/HelaS_param_space_dists.svg')
plt.savefig('output_figs/HelaS_param_space_dists.pdf')
plt.savefig('output_figs/HelaS_param_space_dists.png')

# Plot the parameter space

# In[11]:

packRatio, pLength = zip(*SGoodParams)

options = {'vmin'   : -1.2e4,
           'vmax'   : -4000,
           'origin' : 'lower',
           'extent' : [results['Hela S']['packRatio'].min(), results['Hela S']['packRatio'].max(),
                       results['Hela S']['pLength'].min(),   results['Hela S']['pLength'].max()],
           'aspect' : 'auto'}

fig = plt.figure()

# Log-likelihood map
ax1 = fig.add_axes([0.13, 0.11, 0.84, 0.76])
llhMap = ax1.imshow(results['Hela S']['LLH'], cmap = myCMap, **options)
ax1.set_xticks([10, 30, 50, 70, 90])
ax1.tick_params(axis='x', which='major', pad=0.7)
ax1.tick_params(axis='y', which='major', pad=1.5)

## Plot simulated points
#props = {'alpha' : 0.6,
#         'edgecolors' : None}
#plt.scatter(packRatio, 
#            pLength,
#            s = 10,
#            c = 'white',
#            **props)


# Plot points from distributions
props = {'marker' : '^'}
plt.scatter(c, lp, s = 25, c = 'red', **props)

# Plot contours
levels = [-0.85e4, -0.75e4, -0.65e4, -0.55e4, -0.45e4]
colors = [(0.2, 0.2, 0.2),
          (0.4, 0.4, 0.4),
          (0.6, 0.6, 0.6),
          (0.8, 0.8, 0.8),
          (1.0, 1.0, 1.0)]
plt.contour(CS, LPS, results['Hela S']['LLH'], levels, colors = colors, linewidths = 0.5)

plt.xlim((results['Hela S']['packRatio'].min(), results['Hela S']['packRatio'].max()))
plt.ylim((results['Hela S']['pLength'].min(),   results['Hela S']['pLength'].max()))
plt.xlabel('Packing density, bp/nm', labelpad = 0.5)
plt.ylabel('Persistence length, nm', labelpad = -1)

cbaxes = fig.add_axes([0.13, 0.9, 0.84, 0.05])
cbar = plt.colorbar(llhMap, cax = cbaxes, ticks = [-12000, -10000, -8000, -6000, -4000], orientation = 'horizontal')
cbar.ax.xaxis.set_ticklabels(['', '', '', '', ''])
cbar.ax.xaxis.set_ticks_position('top')

plt.savefig('output_figs/HelaS_param_space.svg')
plt.savefig('output_figs/HelaS_param_space.pdf')
plt.savefig('output_figs/HelaS_param_space.png')
