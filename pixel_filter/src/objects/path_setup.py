'''
Object to define and create directory structure for project.
'''
import os
import sys

class path_setup:
    
    def __init__(self, fileScript=""):
        self.root = os.path.dirname(fileScript)
        self.src = os.path.join(self.root, "src")
        self.inputs = os.path.join(self.root, "inputs")
        self.outputs = os.path.join(self.root, "outputs")
        
        self.check_and_make_dir(self.outputs)
    
    def check_and_make_dir(self, directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        