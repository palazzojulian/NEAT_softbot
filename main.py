from Classes.environment import Env
from Classes.materials import Material
from Classes.simulator import Sim

from Functions.functions import write_voxelyze_file


print("simulation/environment parameters -> simulation.vxa")
print("model -> design -> simulation.vxa -> call voxelyze -> fitness.xml")



##############################################################################################################

#                                _______________________________

##############################################################################################################








##############################################################################################################

#                                SETUP FILE DIRECTORIES

##############################################################################################################


# create file directories
import os

run_directory = 'softrobot'
run_name = 'trialrun'

if not os.path.exists(run_directory):
            os.makedirs(run_directory)
            # store vxa files
            os.makedirs(f"{run_directory}/voxelyzeFiles/")
            # store sim files
            os.makedirs(f"{run_directory}/tempFiles/")
            # results
            os.makedirs(f"{run_directory}/bestFiles/")





## download the compiled voxelyze variant used in: https://arxiv.org/abs/2102.02579
## this variant of voxelyze includes the fitness tracker for distance from: https://github.com/skriegman/evosoro
# ! wget https://github.com/KazuyaHoribe/RegeneratingSoftRobots/blob/master/voxelyze?raw=true
# ! mv voxelyze?raw=true voxelyze

os.system("wget https://github.com/KazuyaHoribe/RegeneratingSoftRobots/blob/master/voxelyze?raw=true")

os.system("mv voxelyze?raw=true voxelyze")


##############################################################################################################

#                       SET UP SIMULATION, ENVIRONMENT, MATERIALS

##############################################################################################################


# Setting up the simulation 
sim = Sim(dt_frac =  0.9, # 'Fraction of the optimal integration step. The lower, the more stable (and slower) the simulation.'
          simulation_time =  0.55, 
          fitness_eval_init_time = 0.05)

# Setting up the environment 
env = Env(sticky_floor = 0, time_between_traces = 0)

# Setting up the available materials, here we use the values form: http://jeffclune.com/publications/2013_Softbots_GECCO.pdf
material_list = [Material(id = 1,
                          name = "Passive_Soft", # Fat like
                          color = [0,1,1], # Cyan
                          stiffness = 1e+007, # units in megapascals (MPa)
                          cte = 0), # Coefficient of thermal expansion i.e. actuation_variance unit = 1/ °C
                 Material(id = 2,
                          name = "Passive_Hard", # Bone like
                          color = [0,0,1], # Blue
                          stiffness = 50e+006,
                          cte = 0),
                 Material(id = 3,
                          name = "Active_+", # Muscle like
                          color = [1,0,0], # Red
                          stiffness = 1e+007, 
                          cte = 0.01),
                 Material(id = 4,
                          name = "Active_-", # Muscle like
                          color = [0,1,0], # Green
                          stiffness = 1e+007,
                          cte = -0.01)]

# build a material_dict for plotting
material_dict = {0: [1,1,1]} # Empty
material_name = ['Empty']
for i in material_list:
   material_dict[i.id] = i.color
   material_name.append(i.name)

n_materials = len(material_dict)
print(n_materials)


#############################################################################################################################

#                                       GENERATE RANDOM SOFTBOT 

#############################################################################################################################

# Generating a random softrobot

import torch
import numpy as np
from matplotlib import pyplot as plt

grid_size = 6 # n voxels in (x, y, z); grid_shape = (grid_size, grid_size, grid_size)

# Generate a random design, this is where the design model (NCA, CPPN, SIREN, .etc) would go in the pipeline
model_output = torch.rand([grid_size*grid_size*grid_size, n_materials])
# model_output = torch.rand([grid_size*grid_size*grid_size, 5])

# Get material class by returning the index for the maxixmum value at each voxel
class_out = torch.argmax(model_output, dim = 1).detach().numpy()

# candidate design to evaluate with voxelyze
candidate_design = class_out.reshape(grid_size,grid_size,grid_size)


#############################################################################################################################

#                                       PLOT CANDIDATE DESIGN (not necessary)

#############################################################################################################################


# 3d voxel plot of model output
fig = plt.figure()
ax = fig.gca(projection='3d')

# map class to material for plotting
design_out = np.array([material_dict[i] for i in class_out])
# reshape to design space
design_out = design_out.reshape(grid_size, grid_size, grid_size, 3) 

# mask empty voxels
filled_mask = np.array(class_out).reshape(grid_size,grid_size,grid_size) > 0 
ax.voxels(filled_mask, facecolors = design_out, edgecolors= 'k')
# add legend
markers = [plt.Line2D([0,0],[0,0], color = color, marker = 's', linestyle = '') for color in list(material_dict.values())[1:]]
ax.legend(markers, material_name[1:], numpoints=1, bbox_to_anchor=(1.35,.75), title = 'Material:');
plt.title('Design candidate')
#ax.view_init(30,41)
plt.show() 

#############################################################################################################################

#                                   WRITE DESIGN TO .VXA FOR VOXELYZE SIMULATOR                                       

#############################################################################################################################

# place holder values
generations = 0
individual_id = 1

vxa_file = f"{run_directory}/voxelyzeFiles/{run_name}--gene_{generations}_id_{individual_id}.vxa"

# create .vxa file
write_voxelyze_file(sim, 
                    env, 
                    generations = generations, 
                    individual_id = individual_id, 
                    candidate_design = candidate_design,
                    im_size = grid_size, 
                    run_directory = run_directory,
                    run_name = run_name,
                    material_list = material_list)



#############################################################################################################################

#                                   RUN SIMULATOR

#############################################################################################################################


import subprocess as sub

# Grant read, write, and execute permission to voxelyze
sub.call("chmod 755 voxelyze", shell=True)
vxa_file = f"{run_directory}/voxelyzeFiles/{run_name}--gene_{generations}_id_{individual_id}.vxa"

def run_physics_sim(vxa_file):
  """
  call voxelyze on a given .vxa file
  returns a .xml file with fitness information saved during the run
  """
  sub.run([f"./voxelyze -f {vxa_file}"], shell = True)

# run physics simulator
run_physics_sim(vxa_file)


# EXTRACT FITNESS METRIC FROM RUN OUTPUT
import lxml
from lxml import etree

fitness_file = f"{run_directory}/tempFiles/softbotsOutput--gene_{generations}_id_{individual_id}.xml"

def get_distance_metric(fitness_file):
  """
  extract and return distance metric from .xml sim run file
  equivalence in evosro is read_voxlyze_results()
  """
  tree = etree.parse(fitness_file)
  distance = float(tree.xpath('//NormFinalDist/text()')[0])

  # delete simulator log file after data extraction
  #sub.run([f"rm {filename}"], shell = True)

  return distance

distance = get_distance_metric(fitness_file)

print(f'distance: {distance}')



#The .vxa simulation file generated by running this notebook be can found at: 
#   - /content/softrobot/voxelyzeFiles/trialrun--gene_0_id_1.vxa

# The fitness file generated from running the physics simulation in this notebook can be found at:
#   - /content/softrobot/tempFiles/softbotsOutput--gene_0_id_1.xml

# It may be helpful to look through these files. 
# Both files are in a .xml format and can be viewed with a text editor (e.g. notepad++). 
# The .vxa file can be imported to voxcad to vizualize the run.












