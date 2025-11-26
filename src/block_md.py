from enum import Enum
import re

from src.inline_md import text_to_textnodes
from src.htmlnode import ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node


RE_HEADING = re.compile(r"^#{1,6}\s(.*)$", re.MULTILINE)
RE_QUOTE = re.compile(r"^>\s?(.*)$", re.MULTILINE)
RE_UL_ITEM = re.compile(r"^[-*]\s(.*)$", re.MULTILINE)
RE_OL_ITEM = re.compile(r"^\d\.\s(.*)$", re.MULTILINE)
RE_CODE_BLOCK = re.compile(r"\`{3}(?:\w+)?\n([^\`]+)\n\`{3}", re.MULTILINE)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def md_to_blocks(markdown_text: str) -> list[str]:
    raw_blocks = markdown_text.split("\n\n")
    result = []
    buffer = []
    is_in_code_block = False
    for block in raw_blocks:
        if block.startswith("```"):
            is_in_code_block = not is_in_code_block
        if is_in_code_block:
            buffer.append(block)
            if block.endswith("```") and block != buffer[0]:
                is_in_code_block = not is_in_code_block
                full_code = "\n\n".join(buffer)
                result.append(full_code.rstrip("\n"))
                buffer = []
            continue
        if not block:
            continue
        result.append(block.strip())
    return result


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith("#"):
        count = len(block) - len(block.lstrip("#"))
        if 1 <= count <= 6 and block[count : count + 1] == " ":
            return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith("> ") and all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    if block.startswith("- ") and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    ordered_prefixes = tuple(f"{i}. " for i in range(1, 10))
    if block.startswith(ordered_prefixes) and all(
        line.startswith(ordered_prefixes) for line in lines
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def md_to_html_node(markdown_text: str) -> ParentNode:
    children = []
    blocks = md_to_blocks(markdown_text)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block_type, block)
        children.append(html_node)
    return ParentNode(tag="div", children=children, props=None)


def block_to_html_node(block_type: BlockType, block_text: str) -> ParentNode:
    match block_type:
        case BlockType.HEADING:
            level = len(block_text) - len(block_text.lstrip("#"))
            text = clean_block_text(block_type, block_text)
            children = text_to_children(text)
            return ParentNode(tag=f"h{level}", children=children)
        case BlockType.CODE:
            text = clean_block_text(block_type, block_text)
            code_node = TextNode(text=text, text_type=TextType.CODE)
            return ParentNode(tag="pre", children=[text_node_to_html_node(code_node)])
        case BlockType.UNORDERED_LIST:
            items = RE_UL_ITEM.findall(block_text)
            list_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            return ParentNode(tag="ul", children=list_nodes)
        case BlockType.ORDERED_LIST:
            items = RE_OL_ITEM.findall(block_text)
            list_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            return ParentNode(tag="ol", children=list_nodes)
        case BlockType.QUOTE:
            text = clean_block_text(block_type, block_text)
            children = text_to_children(text)
            return ParentNode(tag="blockquote", children=children)
        case _:
            text = clean_block_text(block_type, block_text)
            children = text_to_children(text)
            return ParentNode(tag="p", children=children)


def clean_block_text(block_type: BlockType, block_text: str) -> str:
    match block_type:
        case BlockType.HEADING:
            matches = RE_HEADING.findall(block_text)
            return matches[0] if matches else block_text.lstrip("#").strip()
        case BlockType.QUOTE:
            return "\n".join(RE_QUOTE.findall(block_text))
        case BlockType.CODE:
            return "\n".join(RE_CODE_BLOCK.findall(block_text))
        case _:
            return block_text.strip()


def text_to_children(text: str) -> list:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
