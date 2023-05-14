import helper_functions
import sys
import time
import datetime

source_file_path        = ""
destination_file_path   = ""
synchronization_time    = 0


log_file_name = None
log_file      = None
def print_and_log(print_msg=""):
    date_time = datetime.datetime.fromtimestamp(time.time())
    timestamp_formated = date_time.strftime("%d-%m-%Y %H:%M:%S:%f")
    if(print_msg != ""):
        log_file.write(timestamp_formated+" :"+print_msg+"\n")
        log_file.flush()

        print(timestamp_formated+" :"+print_msg)

if __name__ == "__main__":
    # get value from command line.
    command_line_value = sys.argv
    source_file_path                = sys.argv[1]
    destination_file_path           = sys.argv[2]
    synchronization_time            = sys.argv[3]
    log_file_name                   = sys.argv[4]
    print("Logs will be saved in "+log_file_name)
    log_file = open(log_file_name, "a+")

    # 1) Check first if the given source path exist
    source_file_path_is_valid = helper_functions.get_if_given_path_exist(source_file_path)

    # 2) Check if the given destination path exist
    destination_file_path_is_valid = helper_functions.get_if_given_path_exist(destination_file_path)

    # if the desitnation folder is not available, create it
    if(destination_file_path_is_valid==False):
        helper_functions.create_folder_in_given_path(destination_file_path)
        destination_file_path_is_valid = True
    
    # proceed further if both source and destination path are ok
    if((source_file_path_is_valid==True) and (destination_file_path_is_valid==True)):
        while True: # Run the script infinitely
            # Get all the file list from the source folder
            source_file_list = helper_functions.get_all_files_in_given_folder_recursively(source_file_path);
            source_folder_list = helper_functions.get_all_folders_from_given_folder_recursively(source_file_path);

            # Get all the file list from the destination folder
            destination_file_list = helper_functions.get_all_files_in_given_folder_recursively(destination_file_path);
            destination_folder_list = helper_functions.get_all_folders_from_given_folder_recursively(destination_file_path);

            # Prepare file list with common name
            common_files_list_from_source_files_list = []
            common_files_list_from_destination_files_list = []
            for file_from_source_folder in source_file_list:
                src_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(source_file_path, file_from_source_folder)
                for file_from_dest_folder in destination_file_list:
                    des_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(destination_file_path, file_from_dest_folder)
                    if(src_rel_path == des_rel_path):
                        common_files_list_from_source_files_list.append(file_from_source_folder)
                        common_files_list_from_destination_files_list.append(file_from_dest_folder)

            # Prepare file list those are not available in destination folder to copy from source folder
            file_list_to_copy_to_destination_folder = []
            for file_from_source_folder in source_file_list:
                src_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(source_file_path, file_from_source_folder)
                found_source_file_in_destination_file_list = False
                for file_from_dest_folder in destination_file_list:
                    des_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(destination_file_path, file_from_dest_folder)
                    if(src_rel_path==des_rel_path):
                        found_source_file_in_destination_file_list = True
                        break
                # if a file from source file list is not found in destination file list, it has to be copied
                if(found_source_file_in_destination_file_list==False):
                    file_list_to_copy_to_destination_folder.append(file_from_source_folder)

            # Copy the missing files from source folder to destination folder
            for file_path in file_list_to_copy_to_destination_folder:
                helper_functions.copy_from_source_to_destination(source_file_path, destination_file_path, file_path)  
                relativ_path = helper_functions.get_relative_path_with_respect_to_given_path(source_file_path, file_path)
                print_and_log("Copied: "+str(relativ_path)+" to "+destination_file_path)

            file_list_to_delete_from_destination_folder = []
            for file_from_dest_folder in destination_file_list:
                des_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(destination_file_path, file_from_dest_folder)
                found_source_file_in_destination_file_list = False
                for file_from_source_folder in source_file_list:
                    src_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(source_file_path, file_from_source_folder)
                    if(src_rel_path==des_rel_path):
                        found_source_file_in_destination_file_list = True
                        break
                # if a file from destination file list is not found in source file list, it has to be deleted
                if(found_source_file_in_destination_file_list==False):
                    file_list_to_delete_from_destination_folder.append(file_from_dest_folder)

            # delete the unnecessary files from destination folder
            for file_path in file_list_to_delete_from_destination_folder:
                helper_functions.delete_given_file_or_folder(file_path)  
                print_and_log("Deleted: "+str(file_path))

            # After files are deleted, folders are not deleted. So empty folders that are not in source folder list has to be deleted.
            destination_folder_list_to_delete = []
            for folder_from_dest_folder in destination_folder_list:
                des_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(destination_file_path, folder_from_dest_folder)
                folder_found = False
                for folder_from_source_folder in source_folder_list:
                    src_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(source_file_path, folder_from_source_folder)
                    if(src_rel_path == des_rel_path):
                        folder_found = True
                if(folder_found==False):
                    destination_folder_list_to_delete.append(folder_from_dest_folder)

            # delete the unnecessary folders from destination folder
            for folder_path in destination_folder_list_to_delete:
                if(helper_functions.delete_given_file_or_folder(folder_path)):
                    print_and_log("Deleted: "+str(folder_path))

            # Prepare folder(empty) list those are not available in destination folder to copy from source folder
            folder_list_to_copy_to_destination_folder = []
            for folder_from_source_folder in source_folder_list:
                src_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(source_file_path, folder_from_source_folder)
                found_source_folder_in_destination_folder_list = False
                for folder_from_dest_folder in destination_folder_list:
                    des_rel_path = helper_functions.get_relative_path_with_respect_to_given_path(destination_file_path, folder_from_dest_folder)
                    if(src_rel_path==des_rel_path):
                        found_source_folder_in_destination_folder_list = True
                        break
                # if a file from source file list is not found in destination file list, it has to be copied
                if(found_source_folder_in_destination_folder_list==False):
                    folder_list_to_copy_to_destination_folder.append(folder_from_source_folder)

            # Copy the missing empty folder from source folder to destination folder
            for file_path in folder_list_to_copy_to_destination_folder:
                helper_functions.copy_from_source_to_destination(source_file_path, destination_file_path, file_path)  
                relativ_path = helper_functions.get_relative_path_with_respect_to_given_path(source_file_path, file_path)
                print_and_log("Copied: "+str(relativ_path)+" to "+destination_file_path)

            time.sleep(float(synchronization_time)) # sleep till this period and then loop starts again.
