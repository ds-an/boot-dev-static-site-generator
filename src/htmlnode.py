class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value 
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NonImplementedError()

    def props_to_html(self):
        if self.props is None or self.props == "":
            return ""
        formatted_string = ""
        for k in self.props:
            formatted_string += f" {k}=\"{self.props[k]}\""
        return formatted_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children},\
            {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("no value")
        html_string = ""
        if self.tag is None:
            html_string = self.value 
            return html_string
        if not self.props:
            html_string = f"<{self.tag}>{self.value}</{self.tag}>"
            return html_string
        html_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_string

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("no tag")
        if self.children is None:
            raise ValueError("no children")
        html_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_string += child.to_html()
        return html_string + f"</{self.tag}>"
