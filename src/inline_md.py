import re
from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        split_nodes = []
        if len(parts) % 2 == 0:
            raise ValueError("Invalid markdown syntax, formatted section not closed")
        for i, part in enumerate(parts):
            if part in ["", "\n"]:
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(part, old_node.text_type))
            else:
                split_nodes.append(TextNode(part, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matched_image_links = extract_markdown_images(original_text)
        if len(matched_image_links) == 0:
            new_nodes.append(node)
            continue
        for name, link in matched_image_links:
            sections = original_text.split(f"![{name}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(text=sections[0], text_type=TextType.TEXT, url=None)
                )
            new_nodes.append(TextNode(text=name, text_type=TextType.IMAGE, url=link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(
                TextNode(text=original_text, text_type=TextType.TEXT, url=None)
            )
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        matched_links = extract_markdown_links(original_text)
        if len(matched_links) == 0:
            new_nodes.append(node)
            continue
        for name, link in matched_links:
            sections = original_text.split(f"[{name}]({link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(
                    TextNode(text=sections[0], text_type=TextType.TEXT, url=None)
                )
            new_nodes.append(TextNode(text=name, text_type=TextType.LINK, url=link))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(
                TextNode(text=original_text, text_type=TextType.TEXT, url=None)
            )
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
