
import os
import shutil
import numpy as np

"""
criar aqui funções que eliminam e criam directorias

"""


def create_dir(directory_name):
    try:
        os.mkdir(directory_name)
        print("Directory " + ": ", directory_name,  " Created ")
    except FileExistsError:
        print("Directory " + ": ", directory_name,  " already exists")


def move_file_to_dir(abs_current_file_path, abs_destination_file_path):
    shutil.move(abs_current_file_path, abs_destination_file_path)


def clear_dir(abs_directory_path_to_dir):

    for file in os.listdir(abs_directory_path_to_dir):
        os.remove(os.path.join(abs_directory_path_to_dir, file))

    print("All files from '" + abs_directory_path_to_dir + "' directory where deleted!")


def get_nr_of_files(path_to_dir):
    files = np.array(list(os.listdir(path_to_dir)))
    return len(files)


"""
# TEST ...

# CREATE DIRECTORY
parent_dir = "C:/Users/carin/Documents/LEIM/PRJ_2122SV/P/Observacoes/data"
for i in range(34, 125):

    dir_classif = parent_dir + "/data_" + str(i) + "/classif"
    dir_videos = parent_dir + "/data_" + str(i) + "/videos"
    dir_audios = parent_dir + "/data_" + str(i) + "/audios"

    create_dir(dir_classif)
    create_dir(dir_videos)
    create_dir(dir_audios)



# MOVE VIDEO FILES FROM "videos"(THIS PROJECT) TO ANOOTHER DIRECTORY
for i in range(34, 125):

    src_path = "C:/Users/carin/Documents/LEIM/PRJ_2122SV/P/Projetos/ProjetoCurso/videos/padel_" + str(i) + ".mp4"
    dst_path = "C:/Users/carin/Documents/LEIM/PRJ_2122SV/P/Observacoes/data/data_" + str(i) + "/videos/padel_" + str(i) + ".mp4"
    move_file_to_dir(src_path, dst_path) 
"""
