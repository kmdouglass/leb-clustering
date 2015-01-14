"""Code for generating Fig. 1D -- Southern blots for Hela L and Hela S

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rcParams

fontpath = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
prop = font_manager.FontProperties(fname = fontpath)
rcParams['font.family'] = prop.get_name()
rcParams.update({'font.size' : 12})

hl = np.loadtxt('figure_data/HelaL_SBlot', delimiter = ',')
hs = np.loadtxt('figure_data/HelaS_SBlot', delimiter = ',')

NL = hl[:,0]; BlotL = -hl[:,1] + 255
NS = hs[:,0]; BlotS = -hs[:,1] + 255

fig = plt.figure(figsize = (3.5 , 3.5), dpi = 90)
plt.plot(NL, BlotL, label='Hela L', color = "#333333", linewidth = 2.0)
plt.plot(NS, BlotS,
         label='Hela S',
         color = "#333333",
         linewidth = 2.0,
         linestyle = '--')

fig.tight_layout(pad = 1.5)

plt.xlabel('Genomic length, kb')
plt.ylabel('Line profile, pixel intensities')
plt.xlim((0, 70))
plt.grid(True)
plt.legend()
plt.savefig('fig1d.pdf')
plt.close()
