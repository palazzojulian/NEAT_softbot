##############################################################################################################

#                                WRITE DESIGN TO .VXA SIMULATION FILE

##############################################################################################################

# interface for converting a design candidate to vxa file. This is the format read by the voxelyze physics simulation

def write_voxelyze_file(sim, env, generations, individual_id, candidate_design, im_size, run_directory, run_name, material_list, best = False, baseline=False):
    if best:
       voxelyze_file = open(f"{run_directory}/bestFiles/WINNER.vxa", "w")
    
    elif baseline:
        voxelyze_file = open(f"{run_directory}/BaselineDistances/{run_name}--{individual_id}.vxa","w")

    else:
        
        # create .vxa file
        voxelyze_file = open(f"{run_directory}/voxelyzeFiles/{run_name}--gene_{generations}_id_{individual_id}.vxa", "w")
    
    # add file header
    voxelyze_file.write(
        "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n\
        <VXA Version=\"1.0\">\n")
    
    # Write Simulation parameters to file
    voxelyze_file.write(sim.to_xml(run_directory, generations, individual_id))   

    # Write Environment parameters to file
    voxelyze_file.write(env.to_xml())
    
    # Write Material parameters to file
    voxelyze_file.write(
        f"<Palette>\n\
        {[i.material for i in material_list]}\
        </Palette>\n\
        <Structure Compression=\"ASCII_READABLE\">\n\
        <X_Voxels>{im_size}</X_Voxels>\n\
        <Y_Voxels>{im_size}</Y_Voxels>\n\
        <Z_Voxels>{im_size}</Z_Voxels>\n")
    
    # Write material class at each coord (x,y,z) to voxelyze
    voxelyze_file.write("<Data>\n")
    for z in range(im_size):
        voxelyze_file.write("<Layer><![CDATA[")
        for y in range(im_size):
            for x in range(im_size):
                state = int(candidate_design[x][y][z]) 
                voxelyze_file.write(str(state))
        voxelyze_file.write("]]></Layer>\n")
    voxelyze_file.write("</Data>\n")

    voxelyze_file.write(
        "</Structure>\n\
        </VXC>\n\
        </VXA>")
    voxelyze_file.close()
    return voxelyze_file.name #(jp)

##############################################################################################################

#                                RUN PHYSICS SIMULATOR

##############################################################################################################

import subprocess as sub
def run_physics_sim(vxa_file):

    """
    call voxelyze on a given .vxa file
    returns a .xml file with fitness information saved during the run
    """
    # Grant read, write, and execute permission to voxelyze
    sub.call("chmod 755 voxelyze", shell=True)
    # Run simulator
    sub.run([f"./voxelyze -f {vxa_file}"], shell = True)

##############################################################################################################

#                                EXTRACT DISTANCE FROM SIM OUTPUT

##############################################################################################################

import lxml
from lxml import etree
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

##############################################################################################################

#                                PLOT SOFTBOT STRUCTURE

##############################################################################################################

import matplotlib.pyplot as plt
import numpy as np
def plot_softbot(class_out, material_list, grid_size, design_is_tensor=False):
    
    # create dict from material list
    material_dict = {0: [1,1,1]} # Empty
    material_name = ['Empty']
    for i in material_list:
        material_dict[i.id] = i.color
        material_name.append(i.name)
    n_materials = len(material_dict)

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



##############################################################################################################

#                             FEASIBILITY CHECKER FUNCTION

##############################################################################################################

def is_feasible_design(candidate_design):
    grid_size = candidate_design.shape[0]
    # Now go through list of functions checking each design parameter (ie. floating voxel, split robot, etc.)

    def floater_check():
        all_coords = []
        for x in range(candidate_design.shape[0]):
            for y in range(candidate_design.shape[1]):
                for z in range(candidate_design.shape[2]):
                    all_coords.append([x,y,z])

        non_zero = np.where(candidate_design != 0)
        non_zero = list(zip(*non_zero))
        for coords in non_zero:
            top_layer, bottom_layer = False, False
            x,y,z = coords[0], coords[1], coords[2]
            surrounding_coords = [[x-1,y,z], [x+1,y,z], [x,y-1,z], [x,y+1,z], [x,y,z-1], [x,y,z+1]]
            surrounding_coords = [x for x in surrounding_coords if x in all_coords]
            surrounding_voxels = [candidate_design[x,y,z] for x,y,z in surrounding_coords] 
            if sum(surrounding_voxels) == 0:
                # print(f"Floating Voxel detected at [{x},{y},{z}]")
                return False

        return True


    


    def split_check():
        # CHECK 1
        # Split one way (horizontally)
        check1dict = {}
        for sheet in range(candidate_design.shape[0]):
            check1dict[sheet] = np.sum(candidate_design[sheet])
        # print("Check1Dict:", check1dict)


        # CHECK 2
        # Split the other way (horizontally)
        check2dict = {}
        for row in range(candidate_design.shape[1]):
            row_sum = 0
            for layer in range(candidate_design.shape[0]):
                row_sum += np.sum(candidate_design[layer, row])
            check2dict[row] = row_sum
        # print("Check2Dict:", check2dict)


        # CHECK 3
        # Split vertically (if any layer is completely empty aside from the top layer)
        # add up each column, if colsum==0 then Fail
        check3dict = {}
        for z in range(candidate_design.shape[2]-1):
            layer_sum = 0
            for x in range(candidate_design.shape[1]):
                for y in range(candidate_design.shape[2]):
                    layer_sum += candidate_design[x,y,z]
            check3dict[z] = layer_sum
        # print("Check3Dict:", check3dict)

        def dict_checker(check_dict):
            for x, c in check_dict.items():
                if check_dict[0] == 0:
                    # print("Empty bottom layer.")
                    return False
                while c == 0 and x != (len(check_dict)-1):
                    x += 1
                    c = check_dict[x]
                    if c != 0:
                        return False
                    elif x == (len(check_dict)-1):
                        return True
            return True
                        
        results = [dict_checker(x) for x in [check1dict, check2dict, check3dict]]
        # print(results)
        if not all(results):
            return False
        else:
            return True



    # Feasibility Check function calls
    checks = {"floater check" : floater_check(), 
                "split check" : split_check()
                } # add function calls here
    # print(checks)
    if all(checks.values()) == True:
        # print("All checks passed.")
        return True, None
    else:
        failed_checks = [name for name, func in checks.items() if func == False]
        # print(f"Feasibility Check Failed.\nFailed Checks: {failed_checks}")
        return False, failed_checks








##############################################################################################################

#                              PENALTY/DIVERSITY/LEANNESS FUNCTION

##############################################################################################################




def diversity_adjustment(candidate_design, material_list):
    material_counts = {x.id:0 for x in material_list}
    material_counts[0] = 0 # add empty voxel key
    candidate = candidate_design.reshape(-1)

    for x in candidate:
        material_counts[x] += 1

    material_penalties = {x:x/max(material_counts.keys()) for x in sorted(material_counts.keys())}
    material_penalties[4] = 0.95
    # print("COUNTS:",material_counts)
    # print("PENALTIES:",material_penalties)

    penalties = {k:material_counts[k]*material_penalties[k] for k in material_counts} #  multiply values between dictionaries for each key

    penalty = 1 - (sum(penalties.values())/len(candidate))

    # print(penalties,penalty)

    return penalty













