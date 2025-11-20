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
            if part == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(part, old_node.text_type))
            else:
                split_nodes.append(TextNode(part, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
