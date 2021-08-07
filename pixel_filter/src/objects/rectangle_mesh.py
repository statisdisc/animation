import numpy as np

class rectangle_mesh:
    def __init__(
        self,
        resolution = (100, 100),
        cell_size = (1, 1),
        displacement = (0, 0),
        scale = (1,1)
    ):
        self.resolution = np.array(resolution)
        self.cell_size = np.array(cell_size)
        self.displacement = np.array(displacement)
        self.scale = np.array(scale)
        
        self.indices = np.indices(self.resolution)
        
        # Minimum coordinate for each mesh cell
        # Together, x_min and y_min represent the top-left corner of a cell
        self.x_min = self.indices[1]*self.cell_size[0]*self.scale[0] + self.displacement[0]
        self.y_min = self.indices[0]*self.cell_size[1]*self.scale[1] + self.displacement[1]
        
        # Maximum coordinate for each mesh cell
        # Together, x_max and y_max represent the bottom-right corner of a cell
        self.x_max = self.x_min + self.cell_size[0]*self.scale[0]
        self.y_max = self.y_min + self.cell_size[1]*self.scale[1]
        
        # Center coordinates
        self.x_center = 0.5*(self.x_min + self.x_max)
        self.y_center = 0.5*(self.y_min + self.y_max)
        
        # Area of the cells
        self.area = (self.x_max - self.x_min)*(self.y_max - self.y_min)
        
        # Global properties
        self.width  = self.resolution[1]*self.cell_size[0]*self.scale[0]
        self.height = self.resolution[0]*self.cell_size[1]*self.scale[1]
        self.center = self.displacement + 0.5*np.array([self.width, self.height])

    def rectangle_overlap(self, rectangle):
        '''
        Establish the fractional area overlap between each mesh cell and a rectangle
        Solution modified from 
        https://stackoverflow.com/questions/9324339/how-much-do-two-rectangles-overlap/9325084
        
        :param rectangle: The rectangle being compared with for overlap, rectangle_mesh.
        :return: Array of overlap fractions with same resolution as mesh, np.ndarray.
        '''
        area_overlap = np.maximum(0, np.minimum(self.x_max, rectangle.x_max) - np.maximum(self.x_min, rectangle.x_min)) * \
                       np.maximum(0, np.minimum(self.y_max, rectangle.y_max) - np.maximum(self.y_min, rectangle.y_min))
        
        return area_overlap/self.area
    
    def copy(
        self,
        resolution = False,
        cell_size = False,
        displacement = False,
        scale = False
    ):
        '''
        Copy this object with no strings attached.
        '''
        if type(resolution) == bool:
            resolution = self.resolution
        
        if type(cell_size) == bool:
            cell_size = self.cell_size
        
        if type(displacement) == bool:
            displacement = self.displacement
        
        if type(scale) == bool:
            scale = self.scale
        elif isinstance(scale, (int, float)):
            scale = (scale, scale)
        elif isinstance(scale, (list, np.ndarray)):
            if len(scale) == 1:
                scale = (scale[0], scale[0])
            elif len(scale) == 0:
                scale = (1,1)
        
        return rectangle_mesh(
            resolution = resolution,
            cell_size = cell_size,
            displacement = displacement,
            scale = scale,
        )