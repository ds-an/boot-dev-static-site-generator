class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value 
        self.children = children
        self.props = props

    def to_html(self):
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
