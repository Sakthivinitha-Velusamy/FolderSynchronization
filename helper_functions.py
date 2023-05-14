from pathlib import Path
import os # os module to copy and delete files

#function to know if the given path is a directory/folder
def is_directory(path:Path) -> bool: # return type is bool and arg type is Path
    return path.is_dir()

#function to know if the given path is a file
def is_file(path:Path):
    return (path.is_dir()==False) # anything other than folder is a file

# get the list of folders available in the given path
def get_all_folders_from_given_folder(path:Path):
    folder_list = []
    for file_and_folder in path.iterdir():
        if(is_directory(file_and_folder.absolute())):
            folder_list.append(file_and_folder.absolute())
    return folder_list

# get the list of folders available in the given path recursively
def get_all_folders_from_given_folder_recursively(path_text:str):
    path = Path(path_text)
    folder_list = []
    for file_and_folder in path.iterdir():
        if(is_directory(file_and_folder.absolute())):
            folder_list.append(file_and_folder.absolute()) # append the current folder first
            folder_list += get_all_folders_from_given_folder_recursively(file_and_folder.absolute()) # add the list given by the function
    return folder_list

# get the list of files available in the given path
def get_all_files_in_given_folder(path:Path):
    file_list = []
    for file_and_folder in path.iterdir():
        if(is_file(file_and_folder)):
            file_list.append(file_and_folder.absolute())
    return file_list

# get the list of files available in the given path recursively
def get_all_files_in_given_folder_recursively(path_text:str):
    path = Path(path_text)
    file_list = []
    for file_and_folder in path.iterdir():
        if(is_directory(file_and_folder)):
            file_list += get_all_files_in_given_folder_recursively(file_and_folder.absolute())
        else:
            file_list.append(file_and_folder.absolute())
    return file_list

# function to know if the given path exist
def get_if_given_path_exist(path_str:str):
    return Path.exists( Path(path_str))

def create_folder_in_given_path(path_str:str):
    path = Path(path_str)
    # If parents==true, any missing parents of this path are created as needed
    # If exist_ok==true, FileExistsError exceptions will not be thrown
    path.mkdir(parents=True, exist_ok=True)

# function help to get the relative path of given absolute path with respect to the given parent path
def get_relative_path_with_respect_to_given_path(parent_path_str:str, absolute_path_str:str) -> str:
    parent_path     = Path(parent_path_str)
    absolute_path   = Path(absolute_path_str)
    relative_path   = absolute_path.relative_to(parent_path.absolute())
    return relative_path

# function to copy a file from source to destination
def copy_from_source_to_destination(source_path_text:str, destination_path_text:str, file_to_copy_text:str):
    file_to_copy_relative_path = get_relative_path_with_respect_to_given_path(source_path_text, file_to_copy_text)
    destination_path = Path(destination_path_text)
    file_to_copy_absolute_path = Path.joinpath(destination_path.absolute(), file_to_copy_relative_path)
    create_folder_in_given_path(file_to_copy_absolute_path.parent.absolute()) # create folder to copy the files
    system_command = 'cp -f -r '+'"'+str(file_to_copy_text)+'"'+' '+'"'+str(file_to_copy_absolute_path.parent.absolute())+'"'
    os.system(system_command)

# function to delete a file or folde
def delete_given_file_or_folder(file_to_delete_text:str):
    deleted = False
    file_to_delete_path = Path(file_to_delete_text)
    #first check if file or folder is available
    if(file_to_delete_path.exists()==True):
        try :
            if(is_directory(file_to_delete_path)):
                # delete folder : refer https://docs.python.org/3/library/os.html#os.walk
                for root, dirs, files in os.walk(file_to_delete_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.removedirs(file_to_delete_path)
                deleted = True
            else:
                os.remove(file_to_delete_path)
                deleted = True
        except OSError as err:
            print("Error: failed to remove %s - %s." % (err.filename, err.strerror))
    return deleted