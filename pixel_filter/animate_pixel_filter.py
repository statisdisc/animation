'''
Script for visualising the sensitivity of the single column model (SCM) settings.
'''

#Core Python modules
import os
import sys
import time
import numpy as np
import matplotlib.image

#User-made modules
from src.objects.image_mesh import image_mesh
from src.objects.path_setup import path_setup
from src.objects.rectangle_mesh import rectangle_mesh
from src.utilities.save_image import save_image

def pixel_filter(
        image, 
        filter_scale=100., 
        center=False,
        folder_output=""
    ):
    '''
    Filter an image to make it pixelated.
    This is different from traditional pixel filters because the filter width does not 
    have to be an integer, meaning smoothing must be accounted for.
    :param image_name: Image to be filtered, np.ndarray.
    :param filter_width: The width of the pixelation filter (in terms of pixels), float.
    :param center: If False filtering will start from the top left pixel 
                   If True filtering will start from the center of the image, bool.
    :return: Filtered image array.
    '''
    
    print(f"\n\nCreating filter for {image_name}, filter scale {filter_scale}")
    image_filtered = image.copy()
    image_filtered[...,:3] *= 0
    
    print("\nProcessing data")
    mesh_original = image_mesh(image)
    
    if center:
        mesh_zoom = mesh_original.copy(scale=filter_scale, displacement=(1-filter_scale)*mesh_original.center)
        # mesh_zoom = mesh_original.copy(scale=filter_scale, displacement=(1-filter_scale)*mesh_original.center+0.5*filter_scale)
    else:
        mesh_zoom = mesh_original.copy(scale=filter_scale)
    
    # Go through each zoomed pixel to see whether it is on the "screen" and therefore
    # worth processing.
    mesh_on_screen = mesh_zoom.rectangle_overlap(mesh_original.screen)
    
    rectangles_to_process = []
    for y in range(len(mesh_on_screen)):
        for x in range(len(mesh_on_screen[0])):
            if mesh_on_screen[y][x] > 0.:
                rectangles_to_process.append(
                    rectangle_mesh(
                        resolution = (1,1),
                        cell_size = mesh_zoom.cell_size*mesh_zoom.scale,
                        displacement = (mesh_zoom.x_min[y][x], mesh_zoom.y_min[y][x])
                    )
                )
    
    total_rectangles = len(rectangles_to_process)
    for i in range(total_rectangles):
        sys.stdout.write(f"\rProcessing pixel filter {i+1} of {total_rectangles}")
        sys.stdout.flush()
        image_filtered += mesh_original.filter_image(rectangles_to_process[i])
    
    
    image_id = str(filter_scale).replace(".","p")
    image_name_filtered = os.path.join(folder_output, image_name.replace(".", f"_{image_id}."))
    save_image(image_filtered, image_name_filtered)
    
    print("\nCreating graphics")
    
    
    
    
if __name__ == "__main__":
    timeInit = time.time()
    
    image_name = "reegeebee_0-9-11_999793997_metallic_red_176.png"
    
    print("\nReading image data")
    folder = path_setup(__file__)
    image = matplotlib.image.imread(os.path.join(folder.inputs, image_name))
    
    # pixel_filter(image, filter_scale=100., folder_output=folder.outputs)
    
    for x in range(5,100):
    # for x in range(50,100):
    # for x in range(500,1000):
        pixel_filter(image, filter_scale=x, center=True, folder_output=folder.outputs)
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")