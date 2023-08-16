import os
import numpy as np
import matplotlib.pyplot as plt
from reinforced_angle import ReinforcedAngleBar,ReinforcedAnglePlate
from reinforced_angle_ops import ReinforcedAngleOPS
from math import pi,sqrt

# Units
inch = 1
mm = 1/25.4

# Input
E = 29000
Fy = 50
L = 24*inch
a_max = 600*mm

shape_dict = {
    'A': ReinforcedAngleBar('L3x3x1/4',0.75,50),
    'B': ReinforcedAnglePlate('L3x3x1/4',3.00,0.25,Fy),
    'C': ReinforcedAnglePlate('L3x3x1/4',2.00,0.375,Fy),
    }

# Loop through cases
for case in shape_dict:
    shape = shape_dict[case] 

    # Run general calculations
    Py = Fy*shape.A_total
    Pn_unit = shape.Pnz(L,0,0.86)
    ri = shape.rz_reinf
    a_limit = shape.a_limit(L,0.86)

    # Run calculations at each value of a
    N = 240
    a_list_1 = np.linspace(0.1,40*ri,round(N*40*ri/a_max))
    a_list_2 = np.linspace(40.000001*ri,a_max,N-round(N*40*ri/a_max))
    a_list = np.concatenate((a_list_1,a_list_2))
    Pn_AISC_list = np.zeros(N)
    Pe_proposed_list = np.zeros(N)
    Pn_proposed_list = np.zeros(N)
    for i,a in enumerate(a_list):
        Pn_AISC_list[i] = shape.Pnz(L,a)
        Pe_proposed_list[i] = shape.Pez_proposed(L,a)
        Pn_proposed_list[i] = shape.Pnz_proposed(L,a)


    # Make Plot
    plt.rc('font',family='serif')
    plt.rc('mathtext',fontset='dejavuserif')
    plt.rc('axes',labelsize=8)
    plt.rc('axes',titlesize=8)
    plt.rc('legend',fontsize=8)
    plt.rc('xtick',labelsize=8)
    plt.rc('ytick',labelsize=8)

    aisc_color = 'tab:blue'
    proposed_color = 'tab:orange'

    fig = plt.figure(figsize=(3.5,2.5))
    ax = fig.add_axes([0.16,0.17,0.80,0.80])

    # Add shading where a is not permitted by the three-fourths rule 
    if len(a_limit) == 1:
        plt.axvspan(a_limit[0]/mm, a_max/mm, color='lightgray', alpha=0.5, lw=0)
    elif len(a_limit) == 3:
        plt.axvspan(a_limit[0]/mm, a_limit[1]/mm, color='lightgray', alpha=0.5, lw=0)
        plt.axvspan(a_limit[2]/mm, a_max/mm, color='lightgray', alpha=0.5, lw=0)
    else:
        raise Exception(f"Don't know how to handle this a_limit ({a_limit})")

    plt.axhline(1,linestyle='dashed',color='black')
    plt.axhline(Pn_unit/Py,linestyle='dotted',color='black')
    plt.plot(a_list/mm,Pn_AISC_list/Py,color=aisc_color,label='$P_n$ (AISC)')
    if case in ['B','C']:
        plt.plot(a_list/mm,Pe_proposed_list/Py,'--',color=proposed_color,label='$P_e$ (Proposed)')
    plt.plot(a_list/mm,Pn_proposed_list/Py,'-',color=proposed_color,label='$P_n$ (Proposed)')

    plt.xlabel('Distance between connectors, $a$ (mm)')
    plt.ylabel('Normalized axial compression, $P/P_y$')
    plt.xlim((0,a_max/mm))
    plt.ylim((0,1.2))
    plt.legend(loc='lower left',frameon=False)
    plt.savefig(os.path.join('figures', f'design_results_{case}.png'),dpi=300)

plt.show()