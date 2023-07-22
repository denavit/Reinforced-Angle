import matplotlib.pyplot as plt
import numpy as np
from reinforced_angle import ReinforcedAngleBar,ReinforcedAnglePlate

E = 29000
Fy = 50
shape = ReinforcedAngleBar('L3x3x1/4',0.75,50)
#shape = ReinforcedAnglePlate('L3x3x1/4',3.00,0.25,Fy)
#shape = ReinforcedAnglePlate('L3x3x1/4',2.00,0.375,Fy)

Lcz = 24
a_max = 20
Ki = 0.86
K = 1.00


ri = shape.rz_reinf
#store variables
N = 240
a_list_1 = np.linspace(0.1,40*ri,round(N*40*ri/a_max))
a_list_2 = np.linspace(40.000001*ri,a_max,N-round(N*40*ri/a_max))
a_list = np.concatenate((a_list_1,a_list_2))

Lc_over_r_m_list = np.zeros(N)
Ka_over_ri_list = np.zeros(N)
for i,a in enumerate(a_list):
    Lc_over_r_m_list[i] = shape.Lcz_over_rz_m(Lcz,a,Ki)
    Ka_over_ri_list[i] = K*a/ri

a_limit = shape.a_limit(Lcz,Ki,K)
print(a_limit)

#Plot Slenderness vs a
fig = plt.figure(figsize=(5,3))
ax = fig.add_axes([0.15,0.15,0.80,0.80])
plt.plot(a_list,Ka_over_ri_list,label='$Ka/r_{i}$')
plt.plot(a_list,Lc_over_r_m_list,label='$(L_c/r)_{m}$',linestyle='--')
plt.plot(a_list,0.75*Lc_over_r_m_list,label='$0.75(L_c/r)_{m}$',linestyle='--')
for a in a_limit:
    plt.axvline(a,linestyle='dashed',color='black')
plt.xlabel('a (in.)')
plt.ylabel('Slenderness')
plt.xlim((0, a_max))
plt.ylim(bottom=0)
plt.legend(loc='lower right')

plt.show()