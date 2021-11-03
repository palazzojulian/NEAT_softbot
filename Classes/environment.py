class Env(object):
    """Container for VoxCad environment parameters."""
    
    def __init__(self,
                 gravity_enabled = 1, 
                 grav_acc = -27.468, 
                 floor_enabled = 1, 
                 floor_slope = 0.0, 
                 temp_enabled = 1,
                 temp_amp = 39,
                 frequency = 40.0, 
                 time_between_traces = 0,
                 sticky_floor = 0, 
                 lattice_dimension = 0.001, 
                 fat_stiffness = 1e+007, 
                 bone_stiffness = 50e+006,
                 muscle_stiffness = 1e+007, 
                 actuation_variance = 0):
      
      # ENV
      self.gravity_enabled = gravity_enabled
      self.grav_acc = grav_acc
      self.floor_enabled = floor_enabled
      self.floor_slope = floor_slope
      self.temp_enabled = temp_enabled
      self.temp_amp = temp_amp
      self.frequency = frequency
      self.time_between_traces = time_between_traces
      self.sticky_floor = sticky_floor
      self.lattice_dimension = lattice_dimension

    def to_xml(self):
      return str(f"<Environment>\n\
      <Fixed_Regions>\n\
      <NumFixed>0</NumFixed>\n\
      </Fixed_Regions>\n\
      <Forced_Regions>\n\
      <NumForced>0</NumForced>\n\
      </Forced_Regions>\n\
      <Gravity>\n\
      <GravEnabled>{self.gravity_enabled}</GravEnabled>\n\
      <GravAcc>{self.grav_acc}</GravAcc>\n\
      <FloorEnabled>{self.floor_enabled}</FloorEnabled>\n\
      <FloorSlope>{self.floor_slope}</FloorSlope>\n\
      </Gravity>\n\
      <Thermal>\n\
      <TempEnabled>{self.temp_enabled}</TempEnabled>\n\
      <TempAmp>{self.temp_amp}</TempAmp>\n\
      <TempBase>25</TempBase>\n\
      <VaryTempEnabled>1</VaryTempEnabled>\n\
      <TempPeriod>{1.0/self.frequency}</TempPeriod>\n\
      </Thermal>\n\
      <TimeBetweenTraces>{self.time_between_traces}</TimeBetweenTraces>\n\
      <StickyFloor>{self.sticky_floor}</StickyFloor>\n\
      </Environment>\n\
      <VXC Version=\"0.93\">\n\
        <Lattice>\n\
        <Lattice_Dim>{self.lattice_dimension}</Lattice_Dim>\n\
        <X_Dim_Adj>1</X_Dim_Adj>\n\
        <Y_Dim_Adj>1</Y_Dim_Adj>\n\
        <Z_Dim_Adj>1</Z_Dim_Adj>\n\
        <X_Line_Offset>0</X_Line_Offset>\n\
        <Y_Line_Offset>0</Y_Line_Offset>\n\
        <X_Layer_Offset>0</X_Layer_Offset>\n\
        <Y_Layer_Offset>0</Y_Layer_Offset>\n\
        </Lattice>\n\
        <Voxel>\n\
        <Vox_Name>BOX</Vox_Name>\n\
        <X_Squeeze>1</X_Squeeze>\n\
        <Y_Squeeze>1</Y_Squeeze>\n\
        <Z_Squeeze>1</Z_Squeeze>\n\
        </Voxel>\n")
