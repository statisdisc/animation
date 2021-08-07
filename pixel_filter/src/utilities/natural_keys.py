import re

def atoi(text):
    return int(text) if text.isdigit() else text

def id_from_filename(filename, filename_list):
    
    success = False
    for index_start in range(len(filename)):
        for file in filename_list:
            if file[index_start] != filename[index_start]:
                success = True
                break
        if success:
            break
    
    success = False
    for index_end in range(len(filename)):
        for file in filename_list:
            if file[-index_end-1] != filename[-index_end-1]:
                success = True
                break
        if success:
            break
    
    if index_end == 0:
        return filename[index_start:]
    else:
        return filename[index_start:-index_end]

def sort_natural(text_list):
    sort_dict = {}
    for text in text_list:
        sort_dict[atoi(id_from_filename(text, text_list))] = text
    
    text_list_new = []
    for key in sorted(sort_dict):
        text_list_new.append(sort_dict[key])
    
    return text_list_new