
import os

def latest_file_by_type(path, filetype):         #index the files of extension 'filetype' in folder 'path'
    if os.name is not 'ns':
        pathway = (path+filetype)
        list_of_files = {}
        for root, dirs, files in os.walk(path):
            #This iterator causes error when a folder contains no MP4 files
            if files:
                for f in files:
                    fullpath = os.path.join(root, f)
                    if os.path.splitext(fullpath)[1] == '.MP4' and not f.startswith("."):
                        file_timestamp = os.path.getctime(fullpath)
                        list_of_files.update({fullpath:file_timestamp})
                if list_of_files:
                    latest_file = max(list_of_files, key=list_of_files.get)
                    return list_of_files, latest_file
                else:
                    return None, None
        else:
            return None, None
    else:
        return None, None
