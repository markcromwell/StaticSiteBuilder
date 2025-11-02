from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value or ""

        # Raise for non-self-closing tags with no value (e.g., <p></p> invalid)
        if self.value is None and self.tag != "img":
            raise ValueError("LeafNode with tag must have a value")

        props_html = ""
        if self.props:
            props_html = " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

        if self.value is None:
            # Self-closing for img only
            return f"<{self.tag}{props_html}/>"
        else:
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"