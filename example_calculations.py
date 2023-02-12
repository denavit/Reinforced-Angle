from reinforced_angle import ReinforcedAngleBar,ReinforcedAnglePlate

#shape = ReinforcedAngleBar('L3x3x1/4',0.75,50)
shape = ReinforcedAnglePlate('L3x3x1/4',3.00,0.25,50)
   
print('Total Cross-Sectional Properties')
print(f'A  = {shape.A_total:.4f} in.^2')
print(f'Iz = {shape.Iz_total:.4f} in.^4')
print(f'rz = {shape.rz_total:.4f} in.')

print('\nStrength Results')
Lcz = 24
a   = 12
Ki  = 0.86
Lcz_over_rz = Lcz/shape.rz_total
Lcz_over_rz_m = shape.Lcz_over_rz_m(Lcz,a,Ki)
Pnz = shape.Pnz(Lcz,a,Ki)
print(f'{Lcz_over_rz   = :.4f}')
print(f'{Lcz_over_rz_m = :.4f}')
print(f'{Pnz = :.4f} kips')