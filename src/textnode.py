from enum import Enum

from src.htmlnode import LeafNode


class TextType(str, Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f'TextNode(text="{self.text}", text_type={self.text_type.value}, url="{self.url}")'


def text_node_to_html_node(text_node: TextNode) -> LeafNode | None:
    if not isinstance(text_node.text_type, TextType):
        raise ValueError(f"invalid text type: {text_node.text_type}")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text, props=None)
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text, props=None)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text, props=None)
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text, props=None)
    if text_node.text_type == TextType.LINK:
        return LeafNode(
            tag="a", value=text_node.text, props={"href": str(text_node.url)}
        )
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img",
            value="",
            props={"src": str(text_node.url), "alt": text_node.text},
        )
