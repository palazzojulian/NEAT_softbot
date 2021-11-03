import torch
import numpy as np
import pandas as pd
import os
import time
import subprocess as sub
import lxml
from lxml import etree
from Classes.environment import Env
from Classes.materials import Material
from Classes.simulator import Sim
from Functions.functions import write_voxelyze_file, run_physics_sim, get_distance_metric

run_directory = "softrobot"
baseline_data_dir = f"{run_directory}/BaselineDistances/"

if not os.path.exists(baseline_data_dir):
    os.makedirs(f"{run_directory}/BaselineDistances/")


# Setting up the simulation 
sim = Sim(dt_frac =  0.9, # 'Fraction of the optimal integration step. The lower, the more stable (and slower) the simulation.'
          simulation_time =  0.55, 
          fitness_eval_init_time = 0.05)
env = Env(sticky_floor = 0, time_between_traces = 0)
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



def build_random_softbot(grid_size=6, n_materials=5):
    model_output = torch.rand([grid_size*grid_size*grid_size, n_materials])
    class_out = torch.argmax(model_output, dim = 1).detach().numpy()
    candidate_design = class_out.reshape(grid_size,grid_size,grid_size)
    return candidate_design


# Save the data
baseline_dict = {'robot':[],'distance':[]}



grid_size = 6
total_time = time.time()

for robot_id in range(1, 501):
    start_time = time.time()
    candidate_design = build_random_softbot()
    vxa_file = write_voxelyze_file(sim, 
                        env, 
                        generations = 0, 
                        individual_id = 0, 
                        candidate_design = candidate_design,
                        im_size = grid_size, 
                        run_directory = run_directory,
                        run_name = "baseline",
                        material_list = material_list, 
                        best = False, 
                        baseline=True).name
    # print(vxa_file)
    run_physics_sim(vxa_file=vxa_file)
    fitness_file = f"{run_directory}/tempFiles/softbotsOutput--gene_0_id_0.xml"
    print(f"Simulation {robot_id} took {time.time()-start_time} seconds.")
    distance = get_distance_metric(fitness_file=fitness_file)
    print(f"Robot {robot_id} distance: {distance}")
    baseline_dict['robot'].append(robot_id)
    baseline_dict['distance'].append(distance)

print("Total Runtime: ", time.time()-total_time)
# Save data in CSV
df = pd.DataFrame().from_dict(baseline_dict)
df.to_csv('Baseline Results.csv')