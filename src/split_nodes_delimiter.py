from textnode import TextNode, TextType, text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != text_type:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, text_type, node.url))
            if i < len(parts) - 1:
                new_nodes.append(TextNode(delimiter, text_type, node.url))

    return new_nodes
