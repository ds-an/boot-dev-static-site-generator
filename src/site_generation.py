import shutil
import os

def copy_source_to_dest_dir(source, dest):
    if os.path.exists(dest): 
        shutil.rmtree(dest)
    if not os.path.exists(source):
        raise Exception(f"{source} does not exist")
    os.mkdir(dest)
    current_files = []
    current_dirs = []
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            current_files.append(file_path)
        if os.path.isdir(file_path):
            current_dirs.append(file_path)
    for file in current_files:
        shutil.copy(file, dest)
    for dir in current_dirs:
        _, tail = os.path.split(dir)
        new_dest = os.path.join(dest, tail)
        os.mkdir(new_dest)
        copy_source_to_dest_dir(dir, new_dest)
