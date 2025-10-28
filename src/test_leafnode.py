import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("span", "Hello", {"class": "greeting"})
        node2 = LeafNode("span", "Hello", {"class": "greeting"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = LeafNode("span", "Hello", {"class": "greeting"})
        node2 = LeafNode("div", "Hello", {"class": "greeting"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = LeafNode("p", "Sample paragraph", None)
        expected_repr = "LeafNode(p, Sample paragraph, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_not_equal_different_type(self):
        node = LeafNode("p", "Sample paragraph", None)
        self.assertNotEqual(node, "Not a LeafNode")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com"})
        expected_html = '<a href="https://example.com">Click here</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_props(self):
        node = LeafNode("b", "Bold text")
        expected_html = "<b>Bold text</b>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        expected_html = "Just text"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_no_value_raises(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()