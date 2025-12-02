import os
from pathlib import Path
import re

from src.block_md import md_to_html_node


def extract_title(markdown):
    title = re.findall(r"^#{1}\s(.*)$", markdown, flags=re.MULTILINE)
    if not title:
        raise ValueError("there is not H1 header in the markdown")
    return title[0]


def generate_page(basepath, from_path, template_path, dest_path):
    print(
        f"INFO: Generating page from '{from_path}' to '{dest_path}' using {template_path}."
    )

    markdown_content = ""
    template_content = ""
    with open(from_path, "r") as f:
        markdown_content = f.read()
        f.close()

    with open(template_path, "r") as f:
        template_content = f.read()
        f.close()

    html_content = md_to_html_node(markdown_content).to_html()
    page_title = extract_title(markdown_content)

    page_content = template_content.replace("{{ Title }}", page_title)
    page_content = page_content.replace("{{ Content }}", html_content)
    page_content = page_content.replace('href="/', f'href="{basepath}')
    page_content = page_content.replace('src="/', f'href="{basepath}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page_content)
        f.close()


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for file in contents:
        current_source = os.path.join(dir_path_content, file)
        current_dest = os.path.join(dest_dir_path, file)
        if os.path.isfile(current_source) and file.endswith(".md"):
            html_dest_file = Path(current_dest).with_suffix(".html")
            generate_page(basepath, current_source, template_path, html_dest_file)
        if os.path.isdir(current_source):
            generate_pages_recursive(
                basepath, current_source, template_path, current_dest
            )
