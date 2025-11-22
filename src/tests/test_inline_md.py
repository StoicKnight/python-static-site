import pytest

from src.textnode import TextNode, TextType
from src.inline_md import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


@pytest.mark.parametrize(
    "input_nodes, delimiter, text_type, expected_nodes",
    [
        # Case: Single bold word
        (
            [TextNode("This is text with a **bolded** word", TextType.TEXT)],
            "**",
            TextType.BOLD,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        ),
        # Case: Two bold words
        (
            [
                TextNode(
                    "This is text with a **bolded** word and **another**", TextType.TEXT
                )
            ],
            "**",
            TextType.BOLD,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
        ),
        # Case: Multiword bold
        (
            [
                TextNode(
                    "This is text with a **bolded word** and **another**", TextType.TEXT
                )
            ],
            "**",
            TextType.BOLD,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
        ),
        # Case: Italics (different delimiter)
        (
            [TextNode("This is text with an _italic_ word", TextType.TEXT)],
            "_",
            TextType.ITALIC,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        ),
        # Case: Code block
        (
            [TextNode("This is text with a `code block` word", TextType.TEXT)],
            "`",
            TextType.CODE,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        ),
        # Case: Complex list with mixed types
        (
            [
                TextNode("This is a **BOLD** text", TextType.TEXT),
                TextNode("This is a normal text", TextType.TEXT),
                TextNode("Bold Text", TextType.BOLD),
                TextNode(
                    "This is another **BOLD** text with more **bold** text.",
                    TextType.TEXT,
                ),
            ],
            "**",
            TextType.BOLD,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
                TextNode("This is a normal text", TextType.TEXT),
                TextNode("Bold Text", TextType.BOLD),
                TextNode("This is another ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" text with more ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
        ),
    ],
    ids=[
        "single_bold",
        "double_bold",
        "multiword_bold",
        "italic",
        "code_block",
        "mixed_list_complex",
    ],
)
def test_split_nodes_delimiter(input_nodes, delimiter, text_type, expected_nodes):
    new_nodes = split_nodes_delimiter(input_nodes, delimiter, text_type)
    assert new_nodes == expected_nodes


def test_split_nodes_delimiter_chained():
    node = TextNode("**bold** and _italic_", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    expected = [
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
    ]
    assert new_nodes == expected


def test_split_nodes_missing_closing_delimiter():
    node = TextNode("This is an invalid markdown **BOLD text", TextType.TEXT)
    with pytest.raises(Exception, match="Invalid markdown syntax"):
        split_nodes_delimiter([node], "**", TextType.BOLD)


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        ),
        (
            "This is text with a ![rick []roll](https://i.imgur.com/aKaOqIh().gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            [
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        ),
        ("This link is not an image link [Test link](https://test.example.com)", []),
    ],
    ids=["normal image links", "ignore parenthesis", "ignore normal links"],
)
def test_extract_markdown_images(text, expected):
    actual = extract_markdown_images(text)
    assert actual == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        ),
        (
            "This is text with a link [to boo[t dev](htt()ps://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            [
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        ),
        (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            [],
        ),
    ],
    ids=["normal links", "ignore parenthesis", "ignore image links"],
)
def test_extract_markdown_links(text, expected):
    actual = extract_markdown_links(text)
    assert actual == expected


@pytest.mark.parametrize(
    "nodes, expected",
    [
        (
            [
                TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) another link",
                    TextType.TEXT,
                ),
            ],
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" another link", TextType.TEXT),
            ],
        )
    ],
    ids=["2 links"],
)
def test_split_nodes_link(nodes, expected):
    actual = split_nodes_link(nodes)
    assert actual == expected


@pytest.mark.parametrize(
    "nodes, expected",
    [
        (
            [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) image links",
                    TextType.TEXT,
                ),
            ],
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" image links", TextType.TEXT),
            ],
        ),
        (
            [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                    TextType.TEXT,
                )
            ],
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        ),
        (
            [
                TextNode(
                    "![image](https://www.example.COM/IMAGE.PNG)",
                    TextType.TEXT,
                )
            ],
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
        ),
    ],
    ids=["2 images", "1 image", "single image"],
)
def test_split_nodes_image(nodes, expected):
    actual = split_nodes_image(nodes)
    assert actual == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        ),
        (
            "This ![image](https://my.image.png) is very **important** thats why can be _downloaded_ from [this link](https://my.site.com) by using `curl` command",
            [
                TextNode("This ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://my.image.png"),
                TextNode(" is very ", TextType.TEXT),
                TextNode("important", TextType.BOLD),
                TextNode(" thats why can be ", TextType.TEXT),
                TextNode("downloaded", TextType.ITALIC),
                TextNode(" from ", TextType.TEXT),
                TextNode("this link", TextType.LINK, "https://my.site.com"),
                TextNode(" by using ", TextType.TEXT),
                TextNode("curl", TextType.CODE),
                TextNode(" command", TextType.TEXT),
            ],
        ),
    ],
    ids=["test 1", "test 2"],
)
def test_text_to_textnodes(text, expected):
    actual = text_to_textnodes(text)
    assert actual == expected
