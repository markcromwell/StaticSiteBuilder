from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)  

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})   
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text}) 
    else:
        raise ValueError("Unsupported TextType")
    
def split_nodes_image(old_nodes):   
    """
    Splits image nodes into separate alt text and URL text nodes using regular expressions:
    For example, an image node with text "![image](https://i.imgur.com/zjjcJKZ.png)" would be split into two nodes:
        1. A text node with text "image"
        2. A text node with text "https://i.imgur.com/zjjcJKZ.png"
    Similarly, an image node with text "![second image](https://i.imgur.com/
3elNhQu.png)" would be split into:
        1. A text node with text "second image"
        2. A text node with text "https://i.imgur.com/3elNhQu.png"
    So the input:
    old_nodes = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
    Would result in:
    new_nodes = [TextNode("This is text with an ", TextType.TEXT),
                 TextNode("image", TextType.TEXT),
                 TextNode("https://i.imgur.com/zjjcJKZ.png", TextType.TEXT),
                 TextNode(" and another ", TextType.TEXT),
                 TextNode("second image", TextType.TEXT),
                 TextNode("https://i.imgur.com/3elNhQu.png", TextType.TEXT)]
    From the original node:     
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
    """
    import re

    image_pattern = r'!\[(.*?)\]\((.*?)\)'

    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.IMAGE:
            parts = re.split(image_pattern, node.text)
            i = 0
            while i < len(parts):
                if i % 3 == 0:
                    if parts[i]:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
                elif i % 3 == 1:
                    alt_text = parts[i]
                elif i % 3 == 2:
                    image_url = parts[i]
                    new_nodes.append(TextNode(alt_text, TextType.TEXT))
                    new_nodes.append(TextNode(image_url, TextType.TEXT))
                i += 1
        else:
            new_nodes.append(node)
    return new_nodes



def split_nodes_link(old_nodes):   
    """
    Splits link nodes into separate link text and URL text nodes using regular expressions:
    For example, a link node with text "[example](https://example.com)" would be split into two nodes:
        1. A text node with text "example"
        2. A text node with text "https://example.com"
    So the input:
    old_nodes = [TextNode("This is text with a [example](https://example.com) link.", TextType.TEXT)]
    Would result in:
    new_nodes = [TextNode("This is text with a ", TextType.TEXT),
                 TextNode("example", TextType.TEXT),
                 TextNode("https://example.com", TextType.TEXT),
                 TextNode(" link.", TextType.TEXT)]
    From the original node:
    "This is text with a [example](https://example.com) link."
    """
    import re

    link_pattern = r'\[(.*?)\]\((.*?)\)'

    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.LINK:
            parts = re.split(link_pattern, node.text)
            i = 0
            while i < len(parts):
                if i % 3 == 0:
                    if parts[i]:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
                elif i % 3 == 1:
                    link_text = parts[i]
                elif i % 3 == 2:
                    link_url = parts[i]
                    new_nodes.append(TextNode(link_text, TextType.TEXT))
                    new_nodes.append(TextNode(link_url, TextType.TEXT))
                i += 1
        else:
            new_nodes.append(node)
    return new_nodes    



# Module only: tests are in the `src/test_*.py` files and run via the test runner.