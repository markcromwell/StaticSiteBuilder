"""Module containing render functions for converting markdown blocks into HTMLNodes.

These functions convert specific markdown block types (paragraphs, headings, lists, etc.)
into their corresponding HTML node structure, handling inline markup via text_to_children.
"""

import re
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_to_children


def render_paragraph(block_text):
    """Convert a markdown paragraph block into an HTMLNode.
    
    Collapses internal newlines to spaces and handles inline markup.
    """
    content = block_text.replace('\n', ' ')
    return ParentNode('p', text_to_children(content))


def render_heading(block_text):
    """Convert a markdown heading block into an HTMLNode.
    
    Supports heading levels 1-6 via # prefix count. Any content after
    the initial #s and space is treated as the heading text.
    """
    m = re.match(r'^(#{1,6})\s+(.*)', block_text)
    level = len(m.group(1)) if m else 1
    tag = f'h{level}'
    heading_text = m.group(2) if m else block_text
    return ParentNode(tag, text_to_children(heading_text))


def render_code(block_text):
    """Convert a markdown code block into an HTMLNode.
    
    Extracts content between triple backticks, preserving internal newlines
    and formatting. Language tags are currently ignored.
    """
    start = block_text.find('```')
    end = block_text.rfind('```')
    inner = ''
    if start != -1 and end != -1 and end > start:
        inner = block_text[start+3:end]
        if inner.startswith('\n'):
            inner = inner[1:]
    code_text_node = LeafNode(None, inner)
    code_node = ParentNode('code', [code_text_node])
    return ParentNode('pre', [code_node])


def render_quote(block_text):
    """Convert a markdown blockquote into an HTMLNode.
    
    Strips the > prefix from each line, joins with newlines, and wraps
    the content in a blockquote. Don't add an extra <p> wrapper so the
    blockquote contains the inline content directly.
    """
    lines = block_text.splitlines()
    stripped = [re.sub(r'^>\s?', '', ln) for ln in lines]
    joined = '\n'.join(stripped)
    # Put inline children directly under the blockquote (no extra <p>)
    return ParentNode('blockquote', text_to_children(joined))


def render_unordered_list(block_text):
    """Convert a markdown unordered list block into an HTMLNode.
    
    Creates ul/li structure, stripping the "- " prefix from each line
    and handling inline markup within list items.
    """
    items = []
    for line in block_text.splitlines():
        content = re.sub(r'^-\s', '', line)
        items.append(ParentNode('li', text_to_children(content)))
    return ParentNode('ul', items)


def render_ordered_list(block_text):
    """Convert a markdown ordered list block into an HTMLNode.
    
    Creates ol/li structure, stripping the "1. " etc prefix from each line
    and handling inline markup within list items.
    """
    items = []
    for line in block_text.splitlines():
        content = re.sub(r'^\d+\.\s', '', line)
        items.append(ParentNode('li', text_to_children(content)))
    return ParentNode('ol', items)