import numpy as np
from Classes.materials import Material
from Functions.functions import write_voxelyze_file, run_physics_sim, get_distance_metric, plot_softbot


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

# arr = np.array([[
#         [4, 4, 4, 4, 3, 3],
#         [4, 4, 4, 3, 3, 3],
#         [4, 4, 4, 4, 4, 3],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4]],

#        [[4, 4, 4, 4, 4, 4],
#         [4, 0, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4]],

#        [[4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4]],

#        [[4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4]],

#        [[4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4]],

#        [[4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4],
#         [4, 4, 4, 4, 4, 4]]])



# class_out = np.array([4 for x in range(6*6*6)])

# class_out[4]=3
# class_out[5]=3
# class_out[9]=3
# class_out[10]=3
# class_out[11]=3
# class_out[17]=3
# print(class_out)






# # plot_softbot(class_out=class_out, material_list=material_list, grid_size = 6)

# import os
# # os.system("pip install pygad")
# import pygad
# import numpy

# function_inputs = [4,-2,3.5,5,-11,-4.7]
# desired_output = 44

# def fitness_func(solution, solution_idx):
#     output = numpy.sum(solution*function_inputs)
#     fitness = 1.0 / (numpy.abs(output - desired_output) + 0.000001)
#     return fitness

# fitness_function = fitness_func

# def on_start(ga_instance):
#     print("on_start()")

# def on_fitness(ga_instance, population_fitness):
#     print("on_fitness()")

# def on_parents(ga_instance, selected_parents):
#     print("on_parents()")

# def on_crossover(ga_instance, offspring_crossover):
#     print("on_crossover()")

# def on_mutation(ga_instance, offspring_mutation):
#     print("on_mutation()")

# def on_generation(ga_instance):
#     print("on_generation()")

# def on_stop(ga_instance, last_population_fitness):
#     print("on_stop()")

# ga_instance = pygad.GA(num_generations=3,
#                        num_parents_mating=5,
#                        fitness_func=fitness_function,
#                        sol_per_pop=10,
#                        num_genes=len(function_inputs),
#                        on_start=on_start,
#                        on_fitness=on_fitness,
#                        on_parents=on_parents,
#                        on_crossover=on_crossover,
#                        on_mutation=on_mutation,
#                        on_generation=on_generation,
#                        on_stop=on_stop)

# ga_instance.run()




import time

def run():
    time.sleep(5)

if __name__ == "__main__":
    start_time = time.time()
    run()
    print(f"{round(time.time()-start_time)} seconds.")