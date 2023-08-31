from scipy.optimize import fsolve
from math import pi,sqrt
from libdenavit.section.database import angle_database

class ReinforcedAngle:

    @property
    def w_angle(self):
        return sqrt(2)*self.x_bar_angle
        
    @property
    def w_CG(self):
        return (self.A_angle*self.w_angle + self.A_reinf*self.w_reinf)/(self.A_angle + self.A_reinf)
        
    @property
    def Iz_total(self):
        return (self.Iz_angle + self.A_angle*(self.w_angle-self.w_CG)**2 + self.Iz_reinf + self.A_reinf*(self.w_reinf-self.w_CG)**2)
        
    @property
    def A_total(self):
        return self.A_angle + self.A_reinf
        
    @property
    def rz_total(self):
        return sqrt(self.Iz_total/self.A_total)
    
    def Lcz_over_rz_m(self,Lcz,a,Ki):
        if a/self.rz_reinf <= 40:
            return Lcz/self.rz_total
        else:
            return sqrt((Lcz/self.rz_total)**2 + (Ki*a/self.rz_reinf)**2)
            
    def a_limit(self,Lcz,Ki,K=1):
        Lcz_over_rz_o = Lcz/self.rz_total
        ri = self.rz_reinf
        a_limit_1 = 0.75*Lcz_over_rz_o*ri/K    
        a_limit_2 = sqrt(Lcz_over_rz_o**2 / ((K/(0.75*ri))**2-(Ki/ri)**2))
        if a_limit_1 < 40*ri:
            if a_limit_2 < 40*ri:
                a_limit = (a_limit_1,)
            else:
                a_limit = (a_limit_1,40*ri,a_limit_2)
        else:
            if a_limit_2 < 40*ri:
                a_limit = None
            else:
                a_limit = (a_limit_2,)
        return a_limit
    
    def Pnz(self,Lcz,a,Ki=0.86):
        Lcz_over_rz = self.Lcz_over_rz_m(Lcz,a,Ki)
        Fe = pi**2*self.E/Lcz_over_rz**2
        if Lcz_over_rz <= 4.71*sqrt(self.E/self.Fy):
            Fcr = 0.658**(self.Fy/Fe)*self.Fy
        else:
            Fcr = 0.877*Fe
        Pn = Fcr*self.A_total
        return Pn
    
    def Pez_proposed(self,Lcz,a,K=0.5):
        Pcr1 = (pi**2*self.E*self.Iz_total)/Lcz**2
        Pcr2 = (self.A_total/self.A_reinf)*(pi**2*self.E*self.Iz_reinf)/(K*a)**2
        return min(Pcr1,Pcr2)
    
    def Pnz_proposed(self,Lcz,a,K=0.5):
        Fe = self.Pez_proposed(Lcz,a,K)/self.A_total
        if self.Fy/Fe <= 2.25:
            Fcr = self.Fy*0.658**(self.Fy/Fe)
        else:
            Fcr = 0.877*Fe
        Pn = Fcr*self.A_total
        return Pn


class ReinforcedAngleBar(ReinforcedAngle):
    
    def __init__(self,angle_name,D_bar,Fy):
        self.angle_name = angle_name;
        self.b_angle  = angle_database[angle_name.upper()]["b"]
        self.t_angle  = angle_database[angle_name.upper()]["t"]
        self.A_angle  = angle_database[angle_name.upper()]["A"]
        self.x_bar_angle  = angle_database[angle_name.upper()]["x"]
        self.Iz_angle = angle_database[angle_name.upper()]["Iz"]
        self.rz_angle = angle_database[angle_name.upper()]["rz"]
        self.D_bar = D_bar
        self.E  = 29000
        self.Fy = Fy

    @property
    def A_reinf(self):
        return pi/4*self.D_bar**2
        
    @property
    def Iz_reinf(self):
        return pi/64*self.D_bar**4
        
    @property
    def rz_reinf(self):
        return self.D_bar/4
        
    @property
    def w_reinf(self):
        return sqrt(2)*(self.t_angle+self.D_bar/2)
    

class ReinforcedAnglePlate(ReinforcedAngle):
    
    def __init__(self,angle_name,b_plate,t_plate,Fy):
        self.angle_name = angle_name;
        self.b_angle  = angle_database[angle_name.upper()]["b"]
        self.t_angle  = angle_database[angle_name.upper()]["t"]
        self.A_angle  = angle_database[angle_name.upper()]["A"]
        self.x_bar_angle  = angle_database[angle_name.upper()]["x"]
        self.Iz_angle = angle_database[angle_name.upper()]["Iz"]
        self.rz_angle = angle_database[angle_name.upper()]["rz"]
        self.b_plate = b_plate
        self.t_plate = t_plate
        self.E  = 29000
        self.Fy = Fy

    @property
    def A_reinf(self):
        return self.b_plate*self.t_plate
        
    @property
    def Iz_reinf(self):
        return (1/12)*self.b_plate*self.t_plate**3
        
    @property
    def rz_reinf(self):
        return self.t_plate/sqrt(12)

    @property
    def Zz_reinf(self):
        return (1/4)*self.b_plate*self.t_plate**2
        
    @property
    def w_reinf(self):
        return sqrt(2)*self.t_angle + self.b_plate/2 + self.t_plate/2