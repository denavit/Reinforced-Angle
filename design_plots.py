import numpy as np
import matplotlib.pyplot as plt
from reinforced_angle import ReinforcedAngleBar


shape = ReinforcedAngleBar('L3x3x1/4',0.75,50)
   
N = 240

Lc_max = 60
Lc_list = np.linspace(0.1,Lc_max,N)

a_max = 24
a_list = np.linspace(0.1,a_max,N)    

fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0.10,0.15,0.87,0.82])
a_065_list = np.zeros(N)
a_100_list = np.zeros(N)
for i,Lc in enumerate(Lc_list):
    a_065_list[i] = shape.a_limit(Lc,0.65)
    a_100_list[i] = shape.a_limit(Lc,1.0)
plt.plot([0,Lc_max],[12,12],'--k')
plt.plot(Lc_list,a_065_list,label='$K_i$ = 0.65')
plt.plot(Lc_list,a_100_list,label='$K_i$ = 1.0')
plt.xlabel('Effective length about z-axis, $L_{cz}$ (in.)')
plt.ylabel('Limiting connector spacing, $a$ (in.)')
plt.xlim((0,Lc_max))
plt.ylim((0,30))
plt.legend()    
plt.savefig('Figure_1.png',dpi=300)

fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0.10,0.15,0.87,0.82])
Pn_000_list = np.zeros(N)
Pn_065_list = np.zeros(N)
Pn_100_list = np.zeros(N)
for i,Lc in enumerate(Lc_list):
    Pn_000_list[i] = shape.Pnz(Lc,12.0,0.0)
    Pn_065_list[i] = shape.Pnz(Lc,12.0,0.65)
    Pn_100_list[i] = shape.Pnz(Lc,12.0,1.0)
plt.plot(Lc_list,Pn_000_list,label='$a$ = 0')
plt.plot(Lc_list,Pn_065_list,label='$a$ = 12 in., $K_i$ = 0.65')
plt.plot(Lc_list,Pn_100_list,label='$a$ = 12 in., $K_i$ = 1.0')
plt.xlabel('Effective length about z-axis, $L_{cz}$ (in.)')
plt.ylabel('Nominal strength, $P_n$ (kips)')
plt.xlim((0,Lc_max))
plt.legend()
plt.savefig('Figure_2.png',dpi=300)

fig = plt.figure(figsize=(6,4))
ax = fig.add_axes([0.10,0.15,0.87,0.82])
Pn_065_list = np.zeros(N)
Pn_100_list = np.zeros(N)
for i,a in enumerate(a_list):
    Pn_065_list[i] = shape.Pnz(24.0,a,0.65)
    Pn_100_list[i] = shape.Pnz(24.0,a,1.0)
plt.plot(a_list,Pn_065_list,label='$L_{cz}$ = 24 in., $K_i$ = 0.65')
plt.plot(a_list,Pn_100_list,label='$L_{cz}$ = 24 in., $K_i$ = 1.0')
plt.xlabel('Connector spacing, $a$ (in.)')
plt.ylabel('Nominal strength, $P_n$ (kips)')
plt.xlim((0,a_max))
plt.legend()
plt.savefig('Figure_3.png',dpi=300)

plt.show()