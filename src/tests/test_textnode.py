import pytest
from src.textnode import TextNode, TextType, text_node_to_html_node


# --- TextNode Model Tests
@pytest.mark.parametrize(
    "node1, node2",
    [
        (
            TextNode("This is a text node", TextType.BOLD, "/path/to/link"),
            TextNode("This is a text node", TextType.BOLD, "/path/to/link"),
        ),
        (
            TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev"),
            TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev"),
        ),
    ],
    ids=["identical_bold_url", "identical_text_url"],
)
def test_text_node_equality(node1, node2):
    assert node1 == node2


def test_text_node_inequality():
    node1 = TextNode("This is a text node", TextType.ITALIC)
    node2 = TextNode("This is a text node", TextType.BOLD)
    assert node1 != node2


def test_text_node_repr():
    node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
    expected = 'TextNode(text="This is a text node", text_type=text, url="https://www.boot.dev")'
    assert repr(node) == expected


# --- Conversion Logic Tests (TextNode -> HTMLNode) --- #
@pytest.mark.parametrize(
    "text_node, expected_tag, expected_value, expected_props",
    [
        # Case: Plain Text
        (
            TextNode("This is a text node", TextType.TEXT),
            None,
            "This is a text node",
            None,
        ),
        # Case: Bold
        (TextNode("This is bold", TextType.BOLD), "b", "This is bold", None),
        # Case: Image
        (
            TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev"),
            "img",
            "",
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        ),
    ],
    ids=["text_to_html", "bold_to_html", "image_to_html"],
)
def test_text_node_to_html_node(
    text_node, expected_tag, expected_value, expected_props
):
    html_node = text_node_to_html_node(text_node)
    assert html_node.tag == expected_tag
    assert html_node.value == expected_value
    assert html_node.props == expected_props
