import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_image, split_nodes_link


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
        self.assertEqual(repr(html_node), 'LeafNode(None, Hello, World!, None)')

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold Text", TextType.BOLD, None)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), 'LeafNode(b, Bold Text, None)')

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

    def test_split_nodes_image(self):
        old_nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.IMAGE,
            )
        ]
        new_nodes = split_nodes_image(old_nodes)
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.TEXT),
            TextNode("https://i.imgur.com/zjjcJKZ.png", TextType.TEXT),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.TEXT),
            TextNode("https://i.imgur.com/3elNhQu.png", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_link(self):
        old_nodes = [
            TextNode(
                "This is text with a [example](https://example.com) link.",
                TextType.LINK,
            )
        ]
        new_nodes = split_nodes_link(old_nodes)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("example", TextType.TEXT),
            TextNode("https://example.com", TextType.TEXT),
            TextNode(" link.", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)


if __name__ == "__main__":
    unittest.main()