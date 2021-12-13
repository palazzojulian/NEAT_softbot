from matplotlib.pyplot import grid
from Classes.environment import Env
from Classes.materials import Material
from Classes.simulator import Sim
from Functions.functions import diversity_adjustment, write_voxelyze_file, run_physics_sim, get_distance_metric, plot_softbot, is_feasible_design
import neat
import subprocess as sub
import lxml
from lxml import etree
import time

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

# ONLY NEEDS TO BE RUN ONCE TO INSTALL VOXELYZE            
# os.system("wget https://github.com/KazuyaHoribe/RegeneratingSoftRobots/blob/master/voxelyze?raw=true")
# os.system("mv voxelyze?raw=true voxelyze")


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
# print(n_materials)



#############################################################################################################################

#                                       GENERATE/SIMULATE SOFTBOTS USING NEAT-PYTHON

#############################################################################################################################

import neat
import numpy as np
import pandas as pd

grid_size = 6
results = {'generation':[], 'robot':[],'distance':[], 'structure':[], 'is_feasible_design': []}
# generations = 0
def eval_genomes(genomes, config):
    global generations, results
    # results = {'generation':[], 'robot':[],'distance':[]}


    for genome_id, genome in genomes:
        generations = p.generation
        individual_id = genome_id
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # List of voxels
        robot_structure = []

        # Activate the network for each voxel
        for z in range(grid_size):
            for y in range(grid_size):
                for x in range(grid_size):
                    output = net.activate((x,y,z))
                    material = np.argmax(output)
                    robot_structure.append(material)
        
        robot_structure = np.array(robot_structure)
        candidate_design = robot_structure.reshape(grid_size, grid_size, grid_size) # CANDIDATE DESIGN TO WRITE .VXA FILE 


         # FEASIBILITY CHECK

        feasible = is_feasible_design(candidate_design)
        if not feasible[0]:
            print(feasible)
            failed_checks = feasible[1]
            print(f"Generation {p.generation}, Robot {genome_id}, Failed Checks: {failed_checks}")
            results['generation'].append(p.generation)
            results['robot'].append(genome_id)
            results['distance'].append("NA")
            results['structure'].append(robot_structure)
            results['is_feasible_design'].append(failed_checks)
            genome.fitness = 0
            individual_id += 1
            


        else:

            # vxa_file = f"{run_directory}/voxelyzeFiles/{run_name}--gene_{generations}_id_{individual_id}.vxa"

            # WRITE .VXA FILE FOR SIMULATOR
            vxa_file = write_voxelyze_file(sim, 
                                env, 
                                generations = p.generation, 
                                individual_id = genome_id, 
                                candidate_design = candidate_design,
                                im_size = grid_size, 
                                run_directory = run_directory,
                                run_name = run_name,
                                material_list = material_list)
            
            
            vxa_file = f"{run_directory}/voxelyzeFiles/{run_name}--gene_{p.generation}_id_{genome_id}.vxa"


            # RUN PHYSICS SIMULATOR
            run_physics_sim(vxa_file)

            # PARSE XML OUTPUT TO EXTRACT FITNESS (NORM_FINAL_DIST)
            fitness_file = f"{run_directory}/tempFiles/softbotsOutput--gene_{p.generation}_id_{individual_id}.xml"
            distance = get_distance_metric(fitness_file)

            print(f'Generation {p.generation}, Robot {genome_id} distance: {distance}')
            results['generation'].append(p.generation)
            results['robot'].append(genome_id)
            results['distance'].append(distance)
            results['structure'].append(robot_structure)
            results['is_feasible_design'].append("YES")

            # EVALUATE FITNESS
            genome.fitness += abs(distance)

            # DIVERSITY ADJUSTMENT
            adjustment = diversity_adjustment(candidate_design, material_list)
            genome.fitness *= adjustment
            print("ROBOT {} DISTANCE {}. DIVERSITY ADJUSTMENT: {}.".format(individual_id, abs(distance), adjustment))

            individual_id +=1

    df = pd.DataFrame().from_dict(results)
    df.to_csv('Simulation Results.csv')



def run(config_file):
    global p
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Run for up to 100 generations.
    winner = p.run(eval_genomes)#, 100)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winning_structure = []
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for z in range(grid_size):
            for y in range(grid_size):
                for x in range(grid_size):
                    output = winner_net.activate((x,y,z))
                    material = np.argmax(output)
                    winning_structure.append(material)
    winning_structure = np.array(winning_structure)
    winning_design = winning_structure.reshape(grid_size, grid_size, grid_size) # insert in place of "candidate design" when writing .vxa file (we already have the winning .vxa file from before)
    print(winning_design)



    # Save winning design as .vxa
    write_voxelyze_file(sim, 
                        env, 
                        generations = p.generation, 
                        individual_id = 0, 
                        candidate_design = winning_design,
                        im_size = grid_size, 
                        run_directory = run_directory,
                        run_name = run_name,
                        material_list = material_list,
                        best = True)

        # print("input {!r}, expected output {!r}, got {!r}".format(x,y,z, output))

    # plot_softbot(class_out = winning_structure, material_list=material_list,grid_size = grid_size)


    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    # p.run(eval_genomes, 10)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__) 
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    start_time = time.time()
    run(config_path)
    print(f"Total Runtime: {round(time.time()-start_time)} seconds.")





















