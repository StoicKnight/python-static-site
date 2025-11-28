import shutil
import os
from src.copystatic import copy_static_content
from src.page import generate_page

path_dest = "./public"
path_source = "./static"
content_source = "./content/index.md"
content_dest = "./public/index.html"
template_path = "./template.html"


def main():
    if os.path.exists(path_dest):
        print(f"INFO: delete '{path_dest}/' directory and its contents.")
        shutil.rmtree(path_dest)

    print("INFO: copy files from '{path_source}/' to '{path_dest}/'.")
    copy_static_content(path_source, path_dest)

    print(
        f"INFO: generate page content from '{content_source}', using '{template_path}', to '{content_dest}'."
    )
    generate_page(content_source, template_path, content_dest)


if __name__ == "__main__":
    main()
