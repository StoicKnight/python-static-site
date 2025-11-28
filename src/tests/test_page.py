import pytest

from src.page import extract_title


@pytest.mark.parametrize(
    "markdown_text, expected",
    [
        ("# Heading 1", "Heading 1"),
        ("THis is a paragraph and then a \n# Heading 1", "Heading 1"),
    ],
    ids=["simple heading", "multi line"],
)
def test_extract_title(markdown_text, expected):
    actual = extract_title(markdown_text)
    assert actual == expected


@pytest.mark.parametrize(
    "markdown_text",
    [("THis is not a Heading 1")],
    ids=["Heading 1"],
)
def test_extract_title_exception(markdown_text):
    with pytest.raises(ValueError) as e:
        extract_title(markdown_text)
        assert "there is not H1 header in the markdown" == str(e.value)
