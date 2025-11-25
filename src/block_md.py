from enum import Enum
import re

from src.inline_md import text_to_textnodes
from src.htmlnode import ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node


def md_to_blocks(markdown_text: str):
    blocks = markdown_text.split("\n\n")
    result = []
    is_code_block = False
    code_block = ""
    for block in blocks:
        if block.startswith("```"):
            is_code_block = not is_code_block
        if is_code_block:
            code_block += f"{block}\n\n"
            if block.endswith("```"):
                is_code_block = not is_code_block
                result.append(code_block.rstrip("\n"))
                code_block = ""
            continue
        if block == "":
            continue
        block = block.strip()
        result.append(block)
    return result


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    HEADING_4 = "heading_4"
    HEADING_5 = "heading_5"
    HEADING_6 = "heading_6"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str):
    lines = block.split("\n")
    if block.startswith("# "):
        return BlockType.HEADING_1
    elif block.startswith("## "):
        return BlockType.HEADING_2
    elif block.startswith("### "):
        return BlockType.HEADING_3
    elif block.startswith("#### "):
        return BlockType.HEADING_4
    elif block.startswith("##### "):
        return BlockType.HEADING_5
    elif block.startswith("###### "):
        return BlockType.HEADING_6
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith(
        ("1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ")
    ):
        for line in lines:
            if not line.startswith(
                ("1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ")
            ):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def md_to_html_node(markdown_text):
    nodes = []
    blocks = md_to_blocks(markdown_text)
    for block in blocks:
        block_type = block_to_block_type(block)
        nodes.append(create_html_node(block_type, block))
    return ParentNode(tag="div", children=nodes, props=None)


def create_html_node(block_type, block_text):
    clean_text = clean_block_text(block_type, block_text)
    if block_type != BlockType.CODE:
        children = text_to_children(clean_text)
        parent = children_to_parent(children, block_type)
    else:
        code_text_node = TextNode(text=clean_text, text_type=TextType.CODE)
        code_html_node = text_node_to_html_node(code_text_node)
        parent = ParentNode(tag="pre", children=[code_html_node])
    return parent


def clean_block_text(block_type, block_text):
    text = ""
    if block_type in [
        BlockType.HEADING_1,
        BlockType.HEADING_2,
        BlockType.HEADING_3,
        BlockType.HEADING_4,
        BlockType.HEADING_5,
        BlockType.HEADING_6,
    ]:
        text = "\n".join(re.findall(r"^#{1,6}\s(.*)", block_text, flags=re.MULTILINE))
    elif block_type == BlockType.UNORDERED_LIST:
        text = "".join(re.findall(r"^[-*]\s?(.*)$", block_text, flags=re.MULTILINE))
    elif block_type == BlockType.ORDERED_LIST:
        text = "".join(re.findall(r"^\d\.\s?(.*)$", block_text, flags=re.MULTILINE))
    elif block_type == BlockType.QUOTE:
        text = "\n".join(re.findall(r"^>\s?(.*)$", block_text, flags=re.MULTILINE))
    elif block_type == BlockType.CODE:
        text = "\n".join(
            re.findall(
                r"\`{3}(?:\w+)?\n([^\`]+)\n\`{3}", block_text, flags=re.MULTILINE
            )
        )
    else:
        text = block_text

    return text.strip()


def text_to_children(text):
    html_nodes = []
    print(f"Text:\n{text}")
    text_nodes = text_to_textnodes(text)
    print(text_nodes)
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def children_to_parent(children, block_type):
    parent = None
    if block_type == BlockType.HEADING_1:
        parent = ParentNode(tag="h1", children=children)
    if block_type == BlockType.HEADING_2:
        parent = ParentNode(tag="h2", children=children)
    if block_type == BlockType.HEADING_3:
        parent = ParentNode(tag="h3", children=children)
    if block_type == BlockType.HEADING_4:
        parent = ParentNode(tag="h4", children=children)
    if block_type == BlockType.HEADING_5:
        parent = ParentNode(tag="h5", children=children)
    if block_type == BlockType.HEADING_6:
        parent = ParentNode(tag="h6", children=children)
    elif block_type == BlockType.ORDERED_LIST:
        list_nodes = []
        for child in children:
            list_node = ParentNode(tag="li", children=[child])
            list_nodes.append(list_node)
        parent = ParentNode(tag="ol", children=list_nodes)
    elif block_type == BlockType.UNORDERED_LIST:
        list_nodes = []
        for child in children:
            list_node = ParentNode(tag="li", children=[child])
            list_nodes.append(list_node)
        parent = ParentNode(tag="ul", children=list_nodes)
    elif block_type == BlockType.QUOTE:
        parent = ParentNode(tag="blockquote", children=children)
    elif block_type == BlockType.PARAGRAPH:
        parent = ParentNode(tag="p", children=children)
    return parent
