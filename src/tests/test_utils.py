import pytest

from src.textnode import TextNode, TextType
from src.utils import split_nodes_delimiter


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


# class TestSplitNodesDelimiter(unittest.TestCase):
#     def test_delim_bold(self):
#         node = TextNode("This is text with a **bolded** word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
#         self.assertListEqual(
#             [
#                 TextNode("This is text with a ", TextType.TEXT),
#                 TextNode("bolded", TextType.BOLD),
#                 TextNode(" word", TextType.TEXT),
#             ],
#             new_nodes,
#         )
#
#     def test_delim_bold_double(self):
#         node = TextNode(
#             "This is text with a **bolded** word and **another**", TextType.TEXT
#         )
#         new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
#         self.assertListEqual(
#             [
#                 TextNode("This is text with a ", TextType.TEXT),
#                 TextNode("bolded", TextType.BOLD),
#                 TextNode(" word and ", TextType.TEXT),
#                 TextNode("another", TextType.BOLD),
#             ],
#             new_nodes,
#         )
#
#     def test_delim_bold_multiword(self):
#         node = TextNode(
#             "This is text with a **bolded word** and **another**", TextType.TEXT
#         )
#         new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
#         self.assertListEqual(
#             [
#                 TextNode("This is text with a ", TextType.TEXT),
#                 TextNode("bolded word", TextType.BOLD),
#                 TextNode(" and ", TextType.TEXT),
#                 TextNode("another", TextType.BOLD),
#             ],
#             new_nodes,
#         )
#
#     def test_delim_italic(self):
#         node = TextNode("This is text with an _italic_ word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
#         self.assertListEqual(
#             [
#                 TextNode("This is text with an ", TextType.TEXT),
#                 TextNode("italic", TextType.ITALIC),
#                 TextNode(" word", TextType.TEXT),
#             ],
#             new_nodes,
#         )
#
#     def test_delim_bold_and_italic(self):
#         node = TextNode("**bold** and _italic_", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
#         new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
#         self.assertListEqual(
#             [
#                 TextNode("bold", TextType.BOLD),
#                 TextNode(" and ", TextType.TEXT),
#                 TextNode("italic", TextType.ITALIC),
#             ],
#             new_nodes,
#         )
#
#     def test_delim_code(self):
#         node = TextNode("This is text with a `code block` word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#         self.assertListEqual(
#             [
#                 TextNode("This is text with a ", TextType.TEXT),
#                 TextNode("code block", TextType.CODE),
#                 TextNode(" word", TextType.TEXT),
#             ],
#             new_nodes,
#         )
#
#     def test_split_nodes_delimiter(self) -> None:
#         # try:
#         nodes = [
#             TextNode("This is a **BOLD** text", TextType.TEXT),
#             TextNode("This is a normal text", TextType.TEXT),
#             TextNode("Bold Text", TextType.BOLD),
#             TextNode(
#                 "This is another **BOLD** text with more **bold** text.", TextType.TEXT
#             ),
#             # TextNode("This is a sentence with inline `code block`.", TextType.CODE),
#             # TextNode("This is an *italic* sentence", TextType.ITALIC),
#             # TextNode("This is an invalid markdown **BOLD text", TextType.TEXT),
#         ]
#         actual = split_nodes_delimiter(nodes, "**", TextType.BOLD)
#         expected = [
#             TextNode("This is a ", TextType.TEXT),
#             TextNode("BOLD", TextType.BOLD),
#             TextNode(" text", TextType.TEXT),
#             TextNode("This is a normal text", TextType.TEXT),
#             TextNode("Bold Text", TextType.BOLD),
#             TextNode("This is another ", TextType.TEXT),
#             TextNode("BOLD", TextType.BOLD),
#             TextNode(" text with more ", TextType.TEXT),
#             TextNode("bold", TextType.BOLD),
#             TextNode(" text.", TextType.TEXT),
#         ]
#         self.assertEqual(expected, actual)
#
#     # except Exception as e:
#     #     self.assertRaises(Exception, split_nodes_delimiter)
#     #     self.assertEqual(e.args[0], "Invalid markdown syntax")
#
#
# if __name__ == "__main__":
#     unittest.main()
