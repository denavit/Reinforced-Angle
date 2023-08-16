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

# Run OpenSees analyses
for name,shape,Fy_reinf,a,L in zip(name_list,shape_list,Fy_reinf_list,a_list,L_list):
    analysis_obj = ReinforcedAngleOPS(shape,L,a,E,Fy_angle,Fy_reinf)
    results = analysis_obj.run_analysis(0.01*L,1000,percent_load_drop_limit=0.10);
    print(f'{name} {results.maximum_load:.3f} kips')