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