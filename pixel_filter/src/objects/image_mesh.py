import numpy as np
from .rectangle_mesh import rectangle_mesh

class image_mesh(rectangle_mesh):
    def __init__(
        self,
        image,
        resolution = (100, 100),
        cell_size = (1, 1),
        displacement = (0, 0),
        scale = (1,1)
    ):
        super().__init__(
            resolution = (image.shape[0], image.shape[1])
        )
        
        self.image = image
        self.screen = rectangle_mesh(
            resolution = (1, 1),
            cell_size = (self.resolution[1], self.resolution[0])
        )
    
    def filter_image(self, rectangle):
        '''
        Take the mean color of an image over an arbitrary rectangular region.
        :param rectangle: The rectangle over which the image color will be averaged, rectangle_mesh.
        :returns: Image array with same resolution of original image, np.ndarray.
        '''
        overlap = self.rectangle_overlap(rectangle)
        
        image_in_filter = overlap[...,None]*self.image
        mean_color = np.sum(image_in_filter, axis=(0,1)) / np.sum(overlap)
        
        return overlap[...,None]*mean_color[None,...]