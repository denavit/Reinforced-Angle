import numpy as np
import matplotlib.pyplot as plt
from reinforced_angle import ReinforcedAngleBar,ReinforcedAnglePlate
from reinforced_angle_ops import ReinforcedAngleOPS
from math import pi

E = 29000
Fy = 50
#shape = ReinforcedAngleBar('L3x3x1/4',0.75,50)
shape = ReinforcedAnglePlate('L3x3x1/4',3.00,0.25,Fy)
L = 24
a_max = 20

# Run critical load analyses
N = 240
buckling_a_list = np.linspace(0.1,a_max,N)    
buckling_Pcr_list = np.zeros(N)
buckling_Pn_list = np.zeros(N)
for i,a in enumerate(buckling_a_list):
    Pcr1 = (pi**2*E*shape.Iz_total)/L**2
    Pcr2 = (shape.A_total/shape.A_reinf)*(pi**2*E*shape.Iz_reinf)/(0.5*a)**2
    buckling_Pcr_list[i] = min(Pcr1,Pcr2)
    Fe = min(Pcr1,Pcr2)/shape.A_total
    if Fy/Fe <= 2.25:
        Fcr = Fy*0.658**(Fy/Fe)
    else:
        Fcr = 0.877*Fe
    buckling_Pn_list[i] = Fcr*shape.A_total


# Run design calculations
N = 240
design_a_list = np.linspace(0.1,a_max,N)    
design_Pn_065_list = np.zeros(N)
design_Pn_100_list = np.zeros(N)
for i,a in enumerate(design_a_list):
    design_Pn_065_list[i] = shape.Pnz(L,a,0.65)
    design_Pn_100_list[i] = shape.Pnz(L,a,1.0)

# Run OpenSees analyses
N = 20
ops_a_list = np.linspace(0.1,a_max,N)    
ops_Pn_list = np.zeros(N)
for i,a in enumerate(ops_a_list):
    analysis_obj = ReinforcedAngleOPS(shape,L,a,E,Fy)
    results = analysis_obj.run_analysis(0.01*L,1000,percent_load_drop_limit=0.10);
    ops_Pn_list[i] = results.maximum_load

# Make Plot
fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0.10,0.15,0.87,0.82])
plt.plot(design_a_list,design_Pn_065_list,label='Design ($K_i$ = 0.65)')
plt.plot(design_a_list,design_Pn_100_list,label='Design ($K_i$ = 1.0)')
plt.plot(buckling_a_list,buckling_Pcr_list,'-',label='Elastic Buckling, $P_{cr}$')
plt.plot(buckling_a_list,buckling_Pn_list,'-',label='$P_n$ based on $P_{cr}$')
plt.plot(ops_a_list,ops_Pn_list,'-o',label='OpenSees')
plt.xlabel('Distance between connectors, $a$ (in.)')
plt.ylabel('Nominal strength, $P_n$ (kips)')
plt.xlim((0,a_max))
plt.ylim((0,Fy*shape.A_total))
plt.legend()
#plt.savefig('Figure_3.png',dpi=300)

plt.show()