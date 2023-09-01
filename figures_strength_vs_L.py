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
a = 10*inch
L_min = 300*mm
L_max = 2000*mm

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
    
    # Run calculations at each value of L
    N = 240
    L_list = np.linspace(L_min,L_max,N)
    Pn_AISC_0_list = np.zeros(N)
    Pe_proposed_list = np.zeros(N)
    Pn_proposed_list = np.zeros(N)
    for i,L in enumerate(L_list):
        Pn_AISC_0_list[i] = shape.Pnz(L,a=0)
        Pe_proposed_list[i] = shape.Pez_proposed(L,a)
        Pn_proposed_list[i] = shape.Pnz_proposed(L,a)

    # Run OpenSees analyses at each value of L
    N = 10
    L_ops_list = np.linspace(L_min,L_max,N)
    P_ops_list = np.zeros(N)
    for i,L in enumerate(L_ops_list):
        analysis_obj = ReinforcedAngleOPS(shape,L,a,E,Fy)
        results = analysis_obj.run_analysis(0.05*L,10000,percent_load_drop_limit=0.05);
        P_ops_list[i] = results.maximum_load
        #P_ops_list[i] = Py
        
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
    gmnia_color = 'tab:green'

    # Make Analysis Results Plot
    fig = plt.figure(figsize=(3.5,2.5))
    ax = fig.add_axes([0.15,0.17,0.80,0.80])

    # Add shading where a is not permitted by the three-fourths rule 
    L_limit = (0.65*a/shape.rz_reinf)*shape.rz_total/0.75
    plt.axvspan(0, L_limit/mm, color='lightgray', alpha=0.5, lw=0)
    
    plt.plot(L_list/mm,Pn_AISC_0_list/Py,color=aisc_color,label='$P_{AISC,0}$')
    #if case in ['B','C']:
    plt.plot(L_list/mm,Pe_proposed_list/Py,'--',color=proposed_color,label='$P_{e,simple}$')
    plt.plot(L_list/mm,Pn_proposed_list/Py,'-',color=proposed_color,label='$P_{simple}$')
    plt.plot(L_ops_list/mm,P_ops_list/Py,'o-',color=gmnia_color,label='$P_{GMNIA}$',markersize=3)

    plt.xlabel('Member length, $L_c$ (mm)')
    plt.ylabel('Normalized axial compression, $P/P_y$')
    plt.xlim((L_min/mm,L_max/mm))
    plt.ylim((0,1.25))
    plt.legend(loc='lower left',frameon=True,framealpha=1.0)
    plt.savefig(os.path.join('figures', f'strength_vs_L_with_gmnia_{case}.png'),dpi=300)

plt.show()