from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, value=None, children=children, props=props)   
        
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return NotImplemented
        return (self.tag == other.tag and
                self.children == other.children and
                self.props == other.props)
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag to convert to HTML")   
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")
        
        props_str = ''
        if self.props:
            props_str = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
            props_str = ' ' + props_str
        
        opening_tag = f"<{self.tag}{props_str}>"
        closing_tag = f"</{self.tag}>"
        children_html = ''.join(child.to_html() for child in self.children)
        return f"{opening_tag}{children_html}{closing_tag}"
    