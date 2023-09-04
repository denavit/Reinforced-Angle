import os
import numpy as np
import matplotlib.pyplot as plt
from reinforced_angle import ReinforcedAngleBar,ReinforcedAnglePlate
from reinforced_angle_ops import ReinforcedAngleOPS
from math import pi

E = 29000
Fy_angle  = 54.9
Fy_rod    = 59.0
Fy_PL_250 = 51.4
Fy_PL_375 = 56.8

shapeA = ReinforcedAngleBar('L3x3x1/4',0.76,Fy_angle)
shapeB = ReinforcedAnglePlate('L3x3x1/4',3.00,0.244,Fy_angle)
shapeC = ReinforcedAnglePlate('L3x3x1/4',2.00,0.367,Fy_angle)

name_list  = ['A1','A2','A3','A4','A5',
              'B1','B2','B3','B4','B5',
              'C1','C2','C3','C4','C5']
shape_list = [shapeA,shapeA,shapeA,shapeA,shapeA,
              shapeB,shapeB,shapeB,shapeB,shapeB,
              shapeC,shapeC,shapeC,shapeC,shapeC]
Fy_reinf_list = [Fy_rod,Fy_rod,Fy_rod,Fy_rod,Fy_rod,
                 Fy_PL_250,Fy_PL_250,Fy_PL_250,Fy_PL_250,Fy_PL_250,
                 Fy_PL_375,Fy_PL_375,Fy_PL_375,Fy_PL_375,Fy_PL_375]
a_list     = [18.91,9.63,5.53,9.88,9.59,
              18.72,9.50,5.59,9.50,9.84,
              18.59,9.59,5.56,9.63,9.59]
L_list     = [24.06,24.06,24.00,35.94,15.06,
              24.06,24.00,24.06,35.94,15.06,
              24.00,24.00,24.06,36.06,15.06]
P_expr_list = [ 90.642, 91.459, 90.578, 69.382,106.707,
               115.833,111.702,112.127, 89.252,119.638,
                98.706,119.163,115.002, 92.642,107.512]


# Write output file header
with open('compare_to_experiments_output.csv', 'w') as f:
    f.write('Specimen,Lc_in,rz_in,a_in,ri_in,P_expr_kips,P_AISC_kips,P_simple_kips,P_AISC_0_kips,P_GMNIA_kips\n')

# Loop through specimens
for name,shape,Fy_reinf,a,L,P_expr in zip(name_list,shape_list,Fy_reinf_list,a_list,L_list,P_expr_list):
    
    # Run OpenSees analyses
    analysis_obj = ReinforcedAngleOPS(shape,L,a,E,Fy_angle,Fy_reinf)
    results = analysis_obj.run_analysis(0.05*L,10000,percent_load_drop_limit=0.10);
    
    # Make plot
    plt.figure()
    plt.plot(results.lateral_deformation_reinf,results.load,label='Reinforcing')
    plt.plot(results.lateral_deformation_angle,results.load,label='Angle')
    plt.xlabel('Lateral Deformation at Mid-height (in.)')
    plt.ylabel('Applied Axial Load (kips)')
    plt.legend()
    plt.savefig(os.path.join('figures', f'OpenSees_{name}.png'))
    plt.close('all')
    
    # Compute design results
    P_AISC = shape.Pnz(L,a,Ki=0.86)
    P_simple = shape.Pnz_proposed(L,a,0.5)
    P_AISC_0 = shape.Pnz(L,0,Ki=0.86)
    rz = shape.rz_total
    ri = shape.rz_reinf

    # Write results to output file
    with open('compare_to_experiments_output.csv', 'a') as f:
        f.write(f'{name},{L},{rz:.5f},{a},{ri:.5f},{P_expr:.3f},{P_AISC:.3f},{P_simple:.3f},{P_AISC_0:.3f},{results.maximum_load:.3f}\n')