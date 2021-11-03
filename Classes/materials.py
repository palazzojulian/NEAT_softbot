class Material(object):
  """Container for VoxCad Material parameters."""

  def __init__(self, id, name, color, stiffness, cte):   
    self.id = id
    self.name = name
    self.color = color  # e.g [0,0,0]
    self.stiffness = stiffness # units in megapascals (MPa).
    self.cte = cte #Coefficient of thermal expansion i.e. actuation, units in 1/°C
    self.material = self.mat_to_voxcad()
  
  def mat_to_voxcad(self):
        return str(
        f"<Material ID=\"{self.id}\">\n\
            <MatType>0</MatType>\n\
            <Name>{self.name}</Name>\n\
            <Display>\n\
            <Red>{self.color[0]}</Red>\n\
            <Green>{self.color[1]}</Green>\n\
            <Blue>{self.color[2]}</Blue>\n\
            <Alpha>1</Alpha>\n\
            </Display>\n\
            <Mechanical>\n\
            <MatModel>0</MatModel>\n\
            <Elastic_Mod>{self.stiffness}</Elastic_Mod>\n\
            <Plastic_Mod>0</Plastic_Mod>\n\
            <Yield_Stress>0</Yield_Stress>\n\
            <FailModel>0</FailModel>\n\
            <Fail_Stress>0</Fail_Stress>\n\
            <Fail_Strain>0</Fail_Strain>\n\
            <Density>1e+006</Density>\n\
            <Poissons_Ratio>0.35</Poissons_Ratio>\n\
            <CTE>{self.cte}</CTE>\n\
            <uStatic>1</uStatic>\n\
            <uDynamic>0.5</uDynamic>\n\
            </Mechanical>\n\
        </Material>\n")