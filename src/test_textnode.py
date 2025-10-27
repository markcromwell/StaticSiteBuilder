import unittest

from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()