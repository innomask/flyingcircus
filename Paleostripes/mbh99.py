'''
 File Name: mbh99.py
 Description: Warming Stripes for MBH99 data.
 Author: Willy Hagi
 E-mail: hagi.willy@gmail.com
 Github: /willyhagi
'''


## IMPORTING
import pandas  as pd
import seaborn as sns
import numpy   as np
import matplotlib.pyplot as plt


## READ DATA
mbh99 = pd.read_csv('mbh99.txt',
                    delim_whitespace=True, header=None)


## RENAME COLUMNS
mbh99 = mbh99.rename(index=str, columns={0:'Year', 1: 'Temperature'})


## SET STYLE
sns.set(style='ticks', context='talk', rc={"lines.linewidth": 0.7})


## LINE GRAPH
fig, ax = plt.subplots(figsize=(12,5))

sns.lineplot(x=mbh99['Year'],
             y=mbh99['Temperature'],
             color='Black')

ax.axvspan(1000, 1200, alpha=0.25, color='red')
ax.axvspan(1400, 1800, alpha=0.25, color='blue')

ax.set_xlabel('Years')
ax.set_ylabel(r'Global Temperature Anomaly ($\degree$C)')

plt.tight_layout()
#plt.savefig('hockeystick.png')
plt.show()


## HEATMAP
plt.figure(figsize=(12, 5))
#RdYlBu_r, seismic, coolwarm, bwr, RdBu_r

sns.heatmap(data=mbh99['Temperature'][np.newaxis,:],
           cmap='seismic', cbar=False,
           vmin=-.4, vmax=.1, center=0.,
           xticklabels=False, yticklabels=False,
           )

plt.tight_layout()
#plt.savefig('mbh99stripes.png', dpi=300)
plt.show()