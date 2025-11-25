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
        ("# Heading 1", BlockType.HEADING_1),
        ("## Heading 2", BlockType.HEADING_2),
        ("### Heading 3", BlockType.HEADING_3),
        ("#### Heading 4", BlockType.HEADING_4),
        ("##### Heading 5", BlockType.HEADING_5),
        ("###### Heading 6", BlockType.HEADING_6),
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

- _Italic_
- Text
- [Link Item](https://link.to.item.com)

##### Heading 5

1. Text
2. **BOLD**
3. `code`

###### Heading 6

>Not a quote""",
            """<div><h1>Heading 1</h1><p>This is a summary for the document</p><h2>Heading 2</h2><p>This a paragraph. This is a <b>test</b> text.\nThat spans multiple Lines.\n<img src="/path/to/image" alt="image"></img>.</p><blockquote>This is a Quote\nand more quote</blockquote><h3>Heading 3</h3><pre><code>import json\n\ndef main():\n\tprint("Hello World")\n\nif __name__ = __main__:\n\tmain()</code></pre><h4>Heading 4</h4><ul><li><i>Italic</i></li><li>Text</li><li><a href="https://link.to.item.com">Link Item</a></li></ul><h5>Heading 5</h5><ol><li>Text</li><li><b>BOLD</b></li><li><code>code</code></li></ol><h6>Heading 6</h6><p>>Not a quote</p></div>""",
        )
    ],
    ids=["test"],
)
def test_md_to_html_node(markdown, expected):
    actual = md_to_html_node(markdown).to_html()
    assert actual == expected
