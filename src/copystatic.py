import os
import shutil


def copy_static_content(source, dest):
    if not os.path.exists(dest):
        print(f"INFO: create a clean '{dest}/' directory")
        os.mkdir(dest)

    if os.path.exists(source):
        files = os.listdir(source)
        print(f"DEBUG: content from source '{source}/':\n\t{files}")
        for file in files:
            new_source_path = os.path.join(source, file)
            new_dest_path = os.path.join(dest, file)

            if os.path.isfile(new_source_path):
                print(f"INFO:\t{new_source_path} -> {new_dest_path} ")
                shutil.copy(new_source_path, dest)
                print(f"DEBUG: content at destination {dest}:\n\t{os.listdir(dest)}")
            else:
                print(f"INFO: moving into nested '{new_dest_path}/' path.")
                copy_static_content(new_source_path, new_dest_path)
