import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

kips_to_kN = 4.44822

# Read strengths from Excel file
columns = [
    'Specimen',
    'P_expr_kips',
    'P_AISC_kips',
    'P_simple_kips',
    'P_AISC_0_kips',
    'P_OPS_kips']

database = pd.read_excel('compare_to_experiments_output.xlsx', engine='openpyxl', sheet_name='data', usecols=columns)

specimen_name = database['Specimen'].to_numpy()
P_expr_kips   = database['P_expr_kips'].to_numpy()
P_AISC_kips   = database['P_AISC_kips'].to_numpy()
P_simple_kips = database['P_simple_kips'].to_numpy()
P_AISC_0_kips = database['P_AISC_0_kips'].to_numpy()
P_OPS_kips    = database['P_OPS_kips'].to_numpy()

# Make plots
# Based on example from https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html

plt.rc('font',family='serif')
plt.rc('mathtext',fontset='dejavuserif')
plt.rc('axes',labelsize=8)
plt.rc('axes',titlesize=8)
plt.rc('legend',fontsize=7)
plt.rc('xtick',labelsize=7)
plt.rc('ytick',labelsize=7)

x = np.arange(len(specimen_name))

# All strengths
bar_width = 1/6

fig = plt.figure(figsize=(6.5,4.0))
ax = fig.add_axes([0.08,0.11,0.90,0.85])
plt.bar(x-2*bar_width,P_expr_kips,  label=r'$P_{expr}$'  ,width=bar_width)
plt.bar(x-1*bar_width,P_AISC_kips,  label=r'$P_{AISC}$'  ,width=bar_width)
plt.bar(x+0*bar_width,P_simple_kips,label=r'$P_{simple}$',width=bar_width)
plt.bar(x+1*bar_width,P_AISC_0_kips,label=r'$P_{AISC,0}$',width=bar_width)
plt.bar(x+2*bar_width,P_OPS_kips,   label=r'$P_{GMNIA}$' ,width=bar_width)
plt.xticks(x,labels=specimen_name, fontsize=7)
plt.xlabel('Specimen')
plt.ylabel('Strength (kips)')
plt.xlim(-4*bar_width,(len(specimen_name)-1)+4*bar_width)
#plt.ylim(0,1200)
plt.legend(loc='upper left',ncol=2)
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
ax.set_axisbelow(True)
#ax.set_ylim(0, 3500)
plt.ylim(0,130)
plt.grid(axis='y', which='minor',linestyle=':', color='lightgrey', zorder=3)
plt.grid(axis='y', which='major',linestyle='-', zorder=3)
plt.savefig(os.path.join('figures', 'strength_bar_chart_all_US.png'), dpi=200)


# Just experiment and analysis
bar_width = 1/3

fig = plt.figure(figsize=(3.25,2.5))
ax = fig.add_axes([0.16,0.15,0.82,0.82])
plt.bar(x-0.5*bar_width,P_expr_kips*kips_to_kN, label='Experiment' ,width=bar_width)
plt.bar(x+0.5*bar_width,P_OPS_kips*kips_to_kN,  label='Analysis'   ,width=bar_width)
plt.xticks(x,labels=specimen_name)
plt.xlabel('Specimen')
plt.ylabel('Strength (kN)')
plt.xlim(-2*bar_width,(len(specimen_name)-1)+2*bar_width)
plt.ylim(0,600)
plt.legend(loc='upper left',ncol=2,frameon=False)
plt.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
ax.set_axisbelow(True)
plt.grid(axis='y', which='minor',linestyle=':', color='lightgrey', zorder=3)
plt.grid(axis='y', which='major',linestyle='-', zorder=3)
plt.savefig(os.path.join('figures', 'strength_bar_chart_SI.png'), dpi=200)


plt.show()