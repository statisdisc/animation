import os
import sys

def get_files_in_folder(folder, extension=""):
    '''
    Return a list of all files in a folder with a particular extension
    '''
    file_list = []
    
    for file in os.listdir(folder):
        if file.endswith(extension):
            file_list.append(os.path.join(folder, file))
    
    return file_list

def get_folders_in_folder(folder, extension=""):
    '''
    Return a list of all sub-folders in a folder
    '''
    folder_list = []
    
    for file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file)):
            folder_list.append(os.path.join(folder, file))
    
    return folder_list