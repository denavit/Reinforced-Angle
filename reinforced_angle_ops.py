import openseespy.opensees as ops
from reinforced_angle import ReinforcedAngleBar,ReinforcedAnglePlate
from math import pi, sin, sqrt
from libdenavit.OpenSees import circ_patch_2d, AnalysisResults


class ReinforcedAngleOPS():

    def __init__(self,shape,L,a,E,Fy_angle,Fy_reinf=None,dxo_over_L=0.001,dxoa_over_a=0.001):
        self.shape = shape
        self.L  = L
        self.a  = a
        self.E  = E
        self.Fy_angle = Fy_angle
        if Fy_reinf is None:
            self.Fy_reinf = Fy_angle
        else:
            self.Fy_reinf = Fy_reinf

        self.dxo = dxo_over_L*L
        self.dxoa = dxoa_over_a*a

        self.nele_a = 8
        self.nele_o = 8
        self.use_fiber_sections = True
    
    def run_analysis(self,target_disp,num_steps=100,percent_load_drop_limit=None):
        # @todo - make this code work with a = L

        # Computed properties
        nele = self.nele_a + 2*self.nele_o

        if self.nele_a % 2 != 0:
            raise ValueError(f"nele_a must be even ({nele = })")
        if nele > 100:
            raise ValueError(f"number of elements must be less than 100 for current node numbering scheme ({nele = })")
            
        angle_mid_node = 100+self.nele_o+self.nele_a//2
        reinf_mid_node = 200+self.nele_o+self.nele_a//2
        xa = self.shape.w_angle - self.shape.w_CG
        xr = self.shape.w_reinf - self.shape.w_CG

        # Build OpenSees model
        ops.wipe()
        ops.model('basic', '-ndm', 2, '-ndf', 3)

        ops.node(1, 0, 0, '-mass', 1, 1, 1)
        ops.node(2, 0, self.L, '-mass', 1, 1, 1)
        ops.fix(1, 1, 1, 0)
        ops.fix(2, 1, 0, 0)

        for i in range(self.nele_o):
            y = (i/self.nele_o)*0.5*(self.L-self.a)
            xo = sin(pi*y/self.L)*self.dxo
            ops.node(100+i, xa+xo, y, '-mass', 1, 1, 1) # Angle
            ops.node(200+i, xr+xo, y, '-mass', 1, 1, 1) # Reinforcement
        for i in range(self.nele_a):
            y = 0.5*(self.L-self.a) + (i/self.nele_a)*self.a
            xo = sin(pi*y/self.L)*self.dxo
            xor = sin(pi*y/self.L)*self.dxo + sin(pi*i/self.nele_a)*self.dxoa
            ops.node(100+i+self.nele_o, xa+xo, y, '-mass', 1, 1, 1) # Angle
            ops.node(200+i+self.nele_o, xr+xor, y, '-mass', 1, 1, 1) # Reinforcement
        for i in range(self.nele_o+1):
            y = 0.5*(self.L-self.a) + self.a + (i/self.nele_o)*0.5*(self.L-self.a)
            xo = sin(pi*y/self.L)*self.dxo
            ops.node(100+i+self.nele_o+self.nele_a, xa+xo, y, '-mass', 1, 1, 1) # Angle
            ops.node(200+i+self.nele_o+self.nele_a, xr+xo, y, '-mass', 1, 1, 1) # Reinforcement

        ops.geomTransf('Corotational', 100)

        if self.use_fiber_sections:
            # @todo - potentially add residual stresses
        
            #ops.uniaxialMaterial('Elastic', 1, self.E)
            ops.uniaxialMaterial('ElasticPP', 1, self.E, self.Fy_angle/self.E)
            ops.uniaxialMaterial('ElasticPP', 2, self.E, self.Fy_reinf/self.E)

            # Angle
            yo = self.shape.w_angle
            ops.section('Fiber', 1)
            yI = -self.shape.b_angle/sqrt(2) - self.shape.t_angle/sqrt(2)
            zI = -self.shape.b_angle/sqrt(2) + self.shape.t_angle/sqrt(2)
            yJ = -self.shape.b_angle/sqrt(2)
            zJ = -self.shape.b_angle/sqrt(2)
            yK = 0.0
            zK = 0.0
            yL = -sqrt(2)*self.shape.t_angle
            zL = 0.0
            ops.patch('quad', 1, 3, 20, yI-yo, zI, yJ-yo, zJ, yK-yo, zK, yL-yo, zL)
            yI = -sqrt(2)*self.shape.t_angle
            zI = 0.0
            yJ = 0.0
            zJ = 0.0 
            yK = -self.shape.b_angle/sqrt(2)
            zK =  self.shape.b_angle/sqrt(2)
            yL = -self.shape.b_angle/sqrt(2) - self.shape.t_angle/sqrt(2)
            zL =  self.shape.b_angle/sqrt(2) - self.shape.t_angle/sqrt(2)
            ops.patch('quad', 1, 3, 20, yI-yo, zI, yJ-yo, zJ, yK-yo, zK, yL-yo, zL)    

            # Reinforcing
            ops.section('Fiber', 2)
            if isinstance(self.shape,ReinforcedAngleBar):
                circ_patch_2d(2, 10, self.shape.D_bar)
            elif isinstance(self.shape,ReinforcedAnglePlate):
                ops.patch('rect', 2, 20, 1, -0.5*self.shape.t_plate, -0.5*self.shape.b_plate, 0.5*self.shape.t_plate, 0.5*self.shape.b_plate)
            else:
                raise ValueError(f'Unknown type for shape: {type(self.shape)}')
            
        else:
            ops.section('Elastic', 1, self.E, self.shape.A_angle, self.shape.Iz_angle)
            ops.section('Elastic', 2, self.E, self.shape.A_reinf, self.shape.Iz_reinf)

        ops.section('Elastic', 3, self.E, 1000*self.shape.A_total, 1000*self.shape.Iz_total)

        ops.beamIntegration("Lobatto", 1, 1, 3) # Angle
        ops.beamIntegration("Lobatto", 2, 2, 3) # Reinforcement
        ops.beamIntegration("Lobatto", 3, 3, 3) # Rigid Elastic

        # Elements 
        # angle and reinforcement
        for i in range(nele):
            ops.element('mixedBeamColumn', 100+i, 100+i, 101+i, 100, 1)
            ops.element('mixedBeamColumn', 200+i, 200+i, 201+i, 100, 2)
        # "weld" (connection between angle and reinforcement)
        for i in range(self.nele_o):
            ops.element('mixedBeamColumn', 301+i, 101+i, 201+i, 100, 3)
            ops.element('mixedBeamColumn', 300+self.nele_o+self.nele_a+i, 100+self.nele_o+self.nele_a+i, 200+self.nele_o+self.nele_a+i, 100, 3)
        # member ends
        ops.element('mixedBeamColumn', 1, 100, 1, 100, 3)
        ops.element('mixedBeamColumn', 2, 1, 200, 100, 3)
        ops.element('mixedBeamColumn', 3, 100+nele, 2, 100, 3)
        ops.element('mixedBeamColumn', 4, 2, 200+nele, 100, 3)

        # Load
        ops.timeSeries("Linear", 1)
        ops.pattern("Plain", 1, 1)
        ops.load(2, 0.0, -1.0, 0.0)

        # Build the analysis
        ops.constraints("Plain")
        ops.numberer("Plain")
        ops.system("UmfPack")
        ops.test('NormUnbalance', 0.001, 10, 5)
        ops.algorithm("Newton")
        #ops.integrator('DisplacementControl', 2, 2, -target_disp/num_steps)
        ops.integrator('DisplacementControl', reinf_mid_node, 1, target_disp/num_steps)
        ops.analysis("Static")

        '''
        from libdenavit.OpenSees import get_fiber_data
        x, y, A, m = get_fiber_data(2)
        print(x)
        print(y)
        print(A)
        print(m)
        '''

        # Initilize results
        results_load = [0]
        results_axial_deformation = [0]
        results_lateral_deformation_reinf = [0]
        results_lateral_deformation_angle = [0]
        results_axial_load_reinf = [0]
        results_axial_load_angle = [0]
        results_bending_moment_reinf = [0]
        results_bending_moment_angle = [0]
    
        # Run analysis
        for i in range(num_steps):
            ops.analyze(1)
            ops.reactions()
            
            results_load.append(ops.getTime())
            results_axial_deformation.append(-ops.nodeDisp(2, 2))
            results_lateral_deformation_reinf.append(ops.nodeDisp(reinf_mid_node, 1))
            results_lateral_deformation_angle.append(ops.nodeDisp(angle_mid_node, 1))
            results_axial_load_reinf.append(ops.eleForce(200+nele/2,2))
            results_axial_load_angle.append(ops.eleForce(100+nele/2,2))
            results_bending_moment_reinf.append(-ops.eleForce(200+nele/2,3))
            results_bending_moment_angle.append(-ops.eleForce(100+nele/2,3))
            # @todo - potentially better to use ops.eleResponse() to get element local forces

            if percent_load_drop_limit is not None:
                if results_load[-1] < (1-percent_load_drop_limit)*max(results_load):
                    break
            

        # Build results object
        results = AnalysisResults()
        results.maximum_load = max(results_load)
        results.load = results_load
        results.axial_deformation = results_axial_deformation
        results.lateral_deformation_reinf = results_lateral_deformation_reinf
        results.lateral_deformation_angle = results_lateral_deformation_angle
        results.axial_load_reinf = results_axial_load_reinf
        results.axial_load_angle = results_axial_load_angle
        results.bending_moment_reinf = results_bending_moment_reinf
        results.bending_moment_angle = results_bending_moment_angle
        
        return results
        
        

