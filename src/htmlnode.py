class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented yet")
    
        props_str = ' '.join(f'  {key}="{value}"  ' for key, value in self.props.items())
        opening_tag = f"<{self.tag} {props_str}>".strip()
        closing_tag = f"</{self.tag}>"
        children_html = ''.join(child.to_html() for child in self.children)
        return f"{opening_tag}{self.value}{children_html}{closing_tag}"
    
    