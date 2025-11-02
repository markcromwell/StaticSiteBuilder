import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.example.com")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.example.com")
        node2 = TextNode("This is a different text node", TextType.ITALIC, "www.different.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Sample text", TextType.LINK, "https://example.com")
        expected_repr = "TextNode(Sample text, TextType.LINK, https://example.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_not_equal_different_type(self):
        node = TextNode("Sample text", TextType.ITALIC, None)
        self.assertNotEqual(node, "Not a TextNode")

    def test_neq_edge_Case(self):
        node = TextNode("", TextType.ITALIC, None)
        node2 = TextNode("", TextType.BOLD, None)
        self.assertNotEqual(node, node2)

def test_text_node_to_html_node_text(self):
    text_node = TextNode("Hello, World!", TextType.TEXT, None)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(repr(html_node), 'LeafNode(None, Hello, World!, None)')  # Added , None

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold Text", TextType.BOLD, None)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), 'LeafNode(b, Bold Text, None)')  # Added , None
        
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Click Here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), "LeafNode(a, Click Here, {'href': 'https://example.com'})")   
    def test_text_node_to_html_node_image(self):
        text_node = TextNode("An image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), "LeafNode(img, None, {'src': 'https://example.com/image.png', 'alt': 'An image'})")
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")



if __name__ == "__main__":
    unittest.main()