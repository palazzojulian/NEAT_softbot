# updated python3 version of evosoro interface, python2 version: https://github.com/skriegman/evosoro/blob/master/evosoro/

class Sim(object):
    """Container for VoxCad simulation parameters."""

    def __init__(self, 
                 self_collisions_enabled = True, 
                 simulation_time = 10.5,
                 dt_frac = 0.9, 
                 stop_condition = 2,
                 fitness_eval_init_time = 0.5,
                 actuation_start_time = 0, 
                 equilibrium_mode = 0, 
                 min_temp_fact = 0.1,
                 max_temp_fact_change = 0.00001,
                 max_stiffness_change = 10000, 
                 min_elastic_mod = 5e006,
                 max_elastic_mod = 5e008, 
                 afterlife_time = 0, 
                 mid_life_freeze_time = 0):
        
        self.self_collisions_enabled = int(self_collisions_enabled)
        self.simulation_time = simulation_time
        self.dt_frac = dt_frac
        self.stop_condition = int(stop_condition)
        self.fitness_eval_init_time = fitness_eval_init_time
        self.equilibrium_mode = equilibrium_mode
        self.min_temp_fact = min_temp_fact
        self.max_temp_fact_change = max_temp_fact_change
        self.max_stiffness_change = max_stiffness_change
        self.min_elastic_mod = min_elastic_mod
        self.max_elastic_mod = max_elastic_mod
        self.afterlife_time = afterlife_time
        self.mid_life_freeze_time = mid_life_freeze_time
    
    def to_xml(self, run_directory, generations, individual_id):
      return str(f"<Simulator>\n\
        <Integration>\n\
        <Integrator>0</Integrator>\n\
        <DtFrac>{self.dt_frac}</DtFrac>\n\
        </Integration>\n\
        <Damping>\n\
        <BondDampingZ>1</BondDampingZ>\n\
        <ColDampingZ>0.8</ColDampingZ>\n\
        <SlowDampingZ>0.001</SlowDampingZ>\n\
        </Damping>\n\
        <Collisions>\n\
        <SelfColEnabled>{self.self_collisions_enabled}</SelfColEnabled>\n\
        <ColSystem>3</ColSystem>\n\
        <CollisionHorizon>2</CollisionHorizon>\n\
        </Collisions>\n\
        <Features>\n\
        <FluidDampEnabled>0</FluidDampEnabled>\n\
        <PoissonKickBackEnabled>0</PoissonKickBackEnabled>\n\
        <EnforceLatticeEnabled>0</EnforceLatticeEnabled>\n\
        </Features>\n\
        <SurfMesh>\n\
        <CMesh>\n\
        <DrawSmooth>1</DrawSmooth>\n\
        <Vertices/>\n\
        <Facets/>\n\
        <Lines/>\n\
        </CMesh>\n\
        </SurfMesh>\n\
        <StopCondition>\n\
        <StopConditionType>{self.stop_condition}</StopConditionType>\n\
        <StopConditionValue>{self.simulation_time}</StopConditionValue>\n\
        <AfterlifeTime>{self.afterlife_time}</AfterlifeTime>\n\
        <MidLifeFreezeTime>{self.mid_life_freeze_time}</MidLifeFreezeTime>\n\
        <InitCmTime>{self.fitness_eval_init_time}</InitCmTime>\n\
        </StopCondition>\n\
        <EquilibriumMode>\n\
        <EquilibriumModeEnabled>{self.equilibrium_mode}</EquilibriumModeEnabled>\n\
        </EquilibriumMode>\n\
        <GA>\n\
        <WriteFitnessFile>1</WriteFitnessFile>\n\
        <FitnessFileName>{run_directory}/tempFiles/softbotsOutput--gene_{generations}_id_{individual_id}.xml</FitnessFileName>\n\
        <QhullTmpFile>{run_directory}/tempFiles/qhullInput--gene_{generations}_id_{individual_id}.txt</QhullTmpFile>\n\
        <CurvaturesTmpFile>{run_directory}/tempFiles/curvatures--gene{generations}_id_{individual_id}.txt</CurvaturesTmpFile>\n\
        </GA>\n\
        <MinTempFact>{self.min_temp_fact}</MinTempFact>\n\
        <MaxTempFactChange>{self.max_temp_fact_change}</MaxTempFactChange>\n\
        <MaxStiffnessChange>{self.max_stiffness_change}</MaxStiffnessChange>\n\
        <MinElasticMod>{self.min_elastic_mod}</MinElasticMod>\n\
        <MaxElasticMod>{self.max_elastic_mod}</MaxElasticMod>\n\
        <ErrorThreshold>{0}</ErrorThreshold>\n\
        <ThresholdTime>{0}</ThresholdTime>\n\
        <MaxKP>{0}</MaxKP>\n\
        <MaxKI>{0}</MaxKI>\n\
        <MaxANTIWINDUP>{0}</MaxANTIWINDUP>\n\
        </Simulator>\n")