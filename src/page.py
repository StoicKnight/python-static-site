import os
import re

from src.block_md import md_to_html_node


def extract_title(markdown):
    title = re.findall(r"^#{1}\s(.*)$", markdown, flags=re.MULTILINE)
    if not title:
        raise ValueError("there is not H1 header in the markdown")
    return title[0]


def generate_page(from_path, template_path, dest_path):
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
    print(f"DEBUG: html content:\n{page_content}")

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(page_content)
        f.close()
