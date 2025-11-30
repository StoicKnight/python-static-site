import shutil
import os
from src.copystatic import copy_static_content
from src.page import generate_pages_recursive

path_dest = "./public"
path_source = "./static"
content_source = "./content"
content_dest = "./public"
template_path = "./template.html"


def main():
    if os.path.exists(path_dest):
        print(f"INFO: delete '{path_dest}/' directory and its contents.")
        shutil.rmtree(path_dest)

    print(f"INFO: copy files from '{path_source}/' to '{path_dest}/'.")
    copy_static_content(path_source, path_dest)

    generate_pages_recursive(content_source, template_path, content_dest)


if __name__ == "__main__":
    main()
