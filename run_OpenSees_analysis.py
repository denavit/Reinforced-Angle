import matplotlib.pyplot as plt
import numpy as np
from reinforced_angle_ops import ReinforcedAngleOPS
from reinforced_angle import ReinforcedAngleBar,ReinforcedAnglePlate
from libdenavit.OpenSees import plot_deformed_2d, plot_undeformed_2d

E = 29000
Fy = 50
#shape = ReinforcedAngleBar('L3x3x1/4',0.75,Fy)
shape = ReinforcedAnglePlate('L3x3x1/4',3.00,0.25,Fy)
#shape = ReinforcedAnglePlate('L3x3x1/4',2.00,0.375,Fy)

L = 36
a = 16

target_disp = 0.004*L
num_steps = 100

analysis_obj = ReinforcedAngleOPS(shape,L,a,E,Fy)
results = analysis_obj.run_analysis(target_disp,num_steps);

# Plot results
plt.figure()
plt.plot(results.axial_deformation,results.load)
plt.xlabel('Axial Deformation (in.)')
plt.ylabel('Applied Axial Load (kips)')

plt.figure()
plt.plot(results.lateral_deformation_reinf,results.load,label='Reinforcing')
plt.plot(results.lateral_deformation_angle,results.load,label='Angle')
plt.xlabel('Lateral Deformation at Mid-height (in.)')
plt.ylabel('Applied Axial Load (kips)')
plt.legend()

plt.figure()
seperation = np.array(results.lateral_deformation_reinf) - np.array(results.lateral_deformation_angle)
plt.plot(seperation,results.load)
plt.xlabel('Seperation (in.)')
plt.ylabel('Applied Axial Load (kips)')

plt.figure()
plt.plot(results.bending_moment_reinf,results.load,label='Reinforcing')
plt.plot(results.bending_moment_angle,results.load,label='Angle')
plt.xlabel('Bending Moment (kip-in.)')
plt.ylabel('Applied Axial Load (kips)')
plt.legend()

plt.figure()
plt.plot(results.axial_load_reinf,results.load,label='Reinforcing')
plt.plot(results.axial_load_angle,results.load,label='Angle')
plt.xlabel('Axial Load (kips)')
plt.ylabel('Applied Axial Load (kips)')
plt.legend()

plt.figure()
plt.plot(results.bending_moment_reinf,results.axial_load_reinf,label='Reinforcing')
plt.plot(results.bending_moment_angle,results.axial_load_angle,label='Angle')

Py = Fy*shape.A_reinf
Mp = Fy*shape.Zz_reinf
interaction_M = [0,0.9*Mp,Mp]
interaction_P = [Py,0.2*Py,0]
plt.plot(interaction_M,interaction_P,'--',label='Reinforcing')

plt.xlabel('Bending Moment (kip-in.)')
plt.ylabel('Axial Load (kips)')
plt.legend()

plot_deformed_2d()