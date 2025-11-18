from typing import Dict, List


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List | None = None,
        props: Dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        html_strings = []
        for prop in self.props:
            html_strings.append(f'{prop}="{self.props[prop]}"')
        return " " + " ".join(html_strings)

    def __repr__(self) -> str:
        return f'HTMLNode(tag="{self.tag}", value="{self.value}", children={self.children}, props={self.props})'


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: Dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, pops={self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List,
        props: Dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={repr(self.children)}, pops={self.props})"
