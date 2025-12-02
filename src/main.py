import shutil
import sys
import os
from src.copystatic import copy_static_content
from src.page import generate_pages_recursive

path_dest = "./docs"
path_source = "./static"
content_source = "./content"
content_dest = "./docs"
template_path = "./template.html"

if not sys.argv:
    basepath = "/"
else:
    basepath = sys.argv[0]


def main():
    if os.path.exists(path_dest):
        print(f"INFO: delete '{path_dest}/' directory and its contents.")
        shutil.rmtree(path_dest)

    print(f"INFO: copy files from '{path_source}/' to '{path_dest}/'.")
    copy_static_content(path_source, path_dest)

    generate_pages_recursive(basepath, content_source, template_path, content_dest)


if __name__ == "__main__":
    main()
