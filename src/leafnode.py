from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return NotImplemented
        return (self.tag == other.tag and
                self.value == other.value and
                self.props == other.props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value to convert to HTML")
        
        if not self.tag:
            return self.value
        
        opening_tag = f"<{self.tag}>"
        if self.props:
            props_str = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            opening_tag = f"<{self.tag} {props_str}>"
        
        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{self.value}{closing_tag}"
    