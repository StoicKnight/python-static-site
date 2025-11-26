from src.block_md import (
    BlockType,
    block_to_block_type,
    md_to_blocks,
    md_to_html_node,
)
import pytest


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item""",
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                """- This is the first list item in a list block
- This is a list item
- This is another list item""",
            ],
        ),
        (
            """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""",
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        ),
        (
            """```python
from typing import List

def main():
    output: List[str] = ["Hello", "World"]
    print(output)
    
if __name__ == __main__:
    main()
```""",
            [
                """```python
from typing import List

def main():
    output: List[str] = ["Hello", "World"]
    print(output)
    
if __name__ == __main__:
    main()
```""",
            ],
        ),
    ],
    ids=["test 1", "test 2", "code block"],
)
def test_md_to_blocks(text, expected):
    actual = md_to_blocks(text)
    assert actual == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("# Heading 1", BlockType.HEADING),
        ("## Heading 2", BlockType.HEADING),
        ("### Heading 3", BlockType.HEADING),
        ("#### Heading 4", BlockType.HEADING),
        ("##### Heading 5", BlockType.HEADING),
        ("###### Heading 6", BlockType.HEADING),
        (
            """This a paragraph. This is a test text.
That spans multiple Lines.
yes yes yes yes.""",
            BlockType.PARAGRAPH,
        ),
        (
            """```python
import json

def main():
	print("Hello World")

if __name__ = __main__:
	main()
```""",
            BlockType.CODE,
        ),
        (
            """> This is a Quote
> and more quote""",
            BlockType.QUOTE,
        ),
        (
            """- Item 1
- Item 2
- Item 3""",
            BlockType.UNORDERED_LIST,
        ),
        (
            """1. O Item 1
2. O Item 2
3. O Item 3""",
            BlockType.ORDERED_LIST,
        ),
        (">Not a quote", BlockType.PARAGRAPH),
    ],
    ids=[
        "H1",
        "H2",
        "H3",
        "H4",
        "H5",
        "H6",
        "Paragraph",
        "Code",
        "Quote",
        "Unordered List",
        "Ordered List",
        "Not a quote",
    ],
)
def test_block_to_block_type(text, expected):
    actual = block_to_block_type(text)
    assert actual == expected


@pytest.mark.parametrize(
    "markdown, expected",
    [
        (
            """
# Heading 1

This is a summary for the document

## Heading 2

This a paragraph. This is a **test** text.
That spans multiple Lines.
![image](/path/to/image).

> This is a Quote
> and more quote

### Heading 3

```python
import json

def main():
	print("Hello World")

if __name__ = __main__:
	main()
```

#### Heading 4

- This is _Italic_ item
- more items with `code`
- [Link Item](https://link.to.item.com)

##### Heading 5

1. Item one
2. **BOLD** item 2
3. `code` item number three

###### Heading 6

>Not a quote""",
            """<div><h1>Heading 1</h1><p>This is a summary for the document</p><h2>Heading 2</h2><p>This a paragraph. This is a <b>test</b> text.\nThat spans multiple Lines.\n<img src="/path/to/image" alt="image"></img>.</p><blockquote>This is a Quote\nand more quote</blockquote><h3>Heading 3</h3><pre><code>import json\n\ndef main():\n\tprint("Hello World")\n\nif __name__ = __main__:\n\tmain()</code></pre><h4>Heading 4</h4><ul><li>This is <i>Italic</i> item</li><li>more items with <code>code</code></li><li><a href="https://link.to.item.com">Link Item</a></li></ul><h5>Heading 5</h5><ol><li>Item one</li><li><b>BOLD</b> item 2</li><li><code>code</code> item number three</li></ol><h6>Heading 6</h6><p>>Not a quote</p></div>""",
        ),
        (
            """
This is **bolded** paragraph
text in a p
tag here

""",
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p></div>",
        ),
        (
            """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

""",
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        ),
        (
            """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

""",
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        ),
        (
            """
# this is an h1

this is paragraph text

## this is an h2
""",
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        ),
        (
            """
> This is a
> blockquote block

this is paragraph text

""",
            "<div><blockquote>This is a\nblockquote block</blockquote><p>this is paragraph text</p></div>",
        ),
        (
            """
```
This is text that _should_ remain
the **same** even with inline stuff
```
""",
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        ),
    ],
    ids=[
        "full markdown",
        "paragraph",
        "multiple paragraphs",
        "lists",
        "headings",
        "blockquote",
        "code",
    ],
)
def test_md_to_html_node(markdown, expected):
    actual = md_to_html_node(markdown).to_html()
    assert actual == expected
