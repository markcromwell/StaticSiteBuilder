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
            # If the image node's text is empty, return a single empty TEXT node.
            if node.text == "":
                new_nodes.append(TextNode("", TextType.TEXT))
                continue

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
    

def text_to_children(text):
    """Convert inline markdown text into a list of HTMLNode children.

    This is a thin helper that reuses text_to_textnodes and
    text_node_to_html_node to produce LeafNode/ParentNode instances
    appropriate for inclusion in ParentNode children lists.
    """
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


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
            # If the link node's text is empty, return a single empty TEXT node.
            if node.text == "":
                new_nodes.append(TextNode("", TextType.TEXT))
                continue

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
            # If the link node's text is empty, return a single empty TEXT node.
            if node.text == "":
                new_nodes.append(TextNode("", TextType.TEXT))
                continue

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


def text_to_textnodes(text) :
    """
This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)

It should output this list of nodes:

[
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]    
    """
    import re

    # Define regex patterns for common inline Markdown elements (in order of specificity)
    patterns = [
        (r'\*\*(.*?)\*\*', TextType.BOLD),      # **bold**
        (r'_([^_]+)_', TextType.ITALIC),        # _italic_
        (r'`([^`]+)`', TextType.CODE),          # `code`
        (r'!\[([^\]]+)\]\(([^)]+)\)', TextType.IMAGE),  # ![alt](url)
        (r'\[([^\]]+)\]\(([^)]+)\)', TextType.LINK)     # [text](url)
    ]

    # Collect all matches with positions
    all_matches = []
    for pattern, name in patterns:
        for match in re.finditer(pattern, text):
            all_matches.append((match.start(), match.end(), name, match.groups()))

    # Sort by start position
    all_matches.sort(key=lambda x: x[0])

    # Build the split parts, skipping overlaps
    parts = []
    last_end = 0
    for start, end, name, groups in all_matches:
        if start < last_end:
            continue  # Skip overlaps (e.g., link pattern on image)
        if start > last_end:
            parts.append(('plain', text[last_end:start]))
        parts.append((name, groups))
        last_end = end

    if last_end < len(text):
        parts.append(('plain', text[last_end:]))

    new_nodes = []  

    for part in parts:
        new_node = None

        match(part):
            case ('plain', content):
                new_node =TextNode(content, TextType.TEXT)
            case (TextType.BOLD, (content,)):
                new_node = TextNode(content, TextType.BOLD)
            case (TextType.ITALIC, (content,)):
                new_node = TextNode(content, TextType.ITALIC)
            case (TextType.CODE, (content,)):
                new_node = TextNode(content, TextType.CODE)
            case (TextType.IMAGE, (alt_text, url)):
                new_node = TextNode(alt_text, TextType.IMAGE, url)
            case (TextType.LINK, (link_text, url)):
                new_node = TextNode(link_text, TextType.LINK, url)
        
        if new_node is None:
            raise ValueError("Unhandled part type")
        
        new_nodes.append(new_node)

    return new_nodes
       

def markdown_to_blocks(markdown):
    """
    Converts a markdown string to a list of blocks(plain strings). Need to split by double newlines.
    Get rid of leading/trailing whitespace/newlines. Get rid of empty blocks.
    """
    import re

    # Split on one-or-more blank lines. Use a CRLF-safe pattern so Windows
    # line endings are handled, and multiple blank lines collapse to a
    # single separator.
    raw_blocks = re.split(r'(?:\r?\n\s*\r?\n)+', markdown)
    blocks = [block.strip() for block in raw_blocks if block.strip() != '']
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    """
Our static site generator supports 6 types of markdown blocks:

paragraph
heading
code
quote
unordered_list
ordered_list
We need a way to inspect a block of markdown text and determine what type of block it is.

Assignment
Create a BlockType enum with the block types from above.
Create a block_to_block_type function that takes a single block of markdown text as input and returns the BlockType representing the type of block it is. You can assume all leading and trailing whitespace were already stripped (we did that in a previous lesson).
Headings start with 1-6 # characters, followed by a space and then the heading text.
Code blocks must start with 3 backticks and end with 3 backticks.
Every line in a quote block must start with a > character.
Every line in an unordered list block must start with a - character, followed by a space.
Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
If none of the above conditions are met, the block is a normal paragraph.
    """

    import re


    # If the block is empty or whitespace-only, treat it as a paragraph.
    if not block or block.strip() == "":
        return BlockType.PARAGRAPH

    lines = block.splitlines()

    if re.match(r'^(#{1,6})\s', lines[0]):
        return BlockType.HEADING
    elif re.match(r'^```', lines[0]) and re.match(r'```$', lines[-1]):
        return BlockType.CODE
    # Allow blockquote lines that start with '>' optionally followed by a space
    elif all(re.match(r'^>\s?', line) for line in lines):
        return BlockType.QUOTE
    elif all(re.match(r'^-\s', line) for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r'^\d+\.\s', line) for line in lines):
        numbers = [int(re.match(r'^(\d+)\.\s', line).group(1)) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    """Convert a full markdown document into a single parent HTMLNode (a div).

    This builds a ParentNode('div') whose children are block-level nodes
    (p, h1-h6, pre/code, blockquote, ul/ol with li children).
    """
    import re
    from parentnode import ParentNode
    from renderers import (
        render_paragraph, render_heading, render_code,
        render_quote, render_unordered_list, render_ordered_list
    )

    root_children = []
    for block in markdown_to_blocks(markdown):
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            root_children.append(render_paragraph(block))
        elif btype == BlockType.HEADING:
            root_children.append(render_heading(block))
        elif btype == BlockType.CODE:
            root_children.append(render_code(block))
        elif btype == BlockType.QUOTE:
            root_children.append(render_quote(block))
        elif btype == BlockType.UNORDERED_LIST:
            root_children.append(render_unordered_list(block))
        elif btype == BlockType.ORDERED_LIST:
            root_children.append(render_ordered_list(block))

    return ParentNode('div', root_children)

# Module only: tests are in the `src/test_*.py` files and run via the test runner.