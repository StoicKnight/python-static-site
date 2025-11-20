import pytest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


# --- HTMLNode Tests --- #
@pytest.mark.parametrize(
    "props, expected_html",
    [
        (
            {"href": "https://www.google.com", "target": "_blank"},
            ' href="https://www.google.com" target="_blank"',
        ),
        (
            {"class": "header", "id": "main"},
            ' class="header" id="main"',
        ),
    ],
    ids=["href_target", "class_id"],
)
def test_html_node_props_to_html(props, expected_html):
    node = HTMLNode(tag="a", value="text", props=props)
    assert node.props_to_html() == expected_html


def test_html_node_repr():
    node = HTMLNode(
        tag="a",
        value="some text",
        props={"href": "https://www.google.com", "target": "_blank"},
    )
    expected = "HTMLNode(tag=\"a\", value=\"some text\", children=None, props={'href': 'https://www.google.com', 'target': '_blank'})"
    assert repr(node) == expected


# --- LeafNode Tests --- #
@pytest.mark.parametrize(
    "leaf_node, expected_html",
    [
        (
            LeafNode(tag=None, value="Hello, world!"),
            "Hello, world!",
        ),
        (
            LeafNode(tag="p", value="This is a paragraph of text."),
            "<p>This is a paragraph of text.</p>",
        ),
        (
            LeafNode(
                tag="a", value="Click me!", props={"href": "https://www.google.com"}
            ),
            '<a href="https://www.google.com">Click me!</a>',
        ),
    ],
    ids=["raw_text", "paragraph", "anchor_with_props"],
)
def test_leaf_to_html(leaf_node, expected_html):
    assert leaf_node.to_html() == expected_html


# --- ParentNode Tests --- #
def test_parent_node_repr():
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])

    expected = "ParentNode(tag=div, children=[ParentNode(tag=span, children=[LeafNode(tag=b, value=grandchild, props=None)], props=None)], props=None)"
    assert repr(parent_node) == expected


@pytest.mark.parametrize(
    "child_structure, expected_html",
    [
        # Case: Direct children
        (
            [LeafNode("span", "child")],
            "<div><span>child</span></div>",
        ),
        # Case: Grandchildren (Nested Parents)
        (
            [ParentNode("span", [LeafNode("b", "grandchild")])],
            "<div><span><b>grandchild</b></span></div>",
        ),
    ],
    ids=["direct_children", "nested_grandchildren"],
)
def test_parent_node_nesting(child_structure, expected_html):
    parent_node = ParentNode("div", child_structure)
    assert parent_node.to_html() == expected_html


@pytest.mark.parametrize(
    "parent_tag, expected_html",
    [
        (
            "p",
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        ),
        (
            "h2",
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        ),
    ],
    ids=["paragraph_multi", "heading_multi"],
)
def test_parent_node_many_children(parent_tag, expected_html):
    children = [
        LeafNode(tag="b", value="Bold text"),
        LeafNode(tag=None, value="Normal text"),
        LeafNode(tag="i", value="italic text"),
        LeafNode(tag=None, value="Normal text"),
    ]
    node = ParentNode(parent_tag, children)
    assert node.to_html() == expected_html
