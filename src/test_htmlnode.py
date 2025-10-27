import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "Hello", [], {"class": "greeting"})
        node2 = HTMLNode("div", "Hello", [], {"class": "greeting"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("div", "Hello", [], {"class": "greeting"})
        node2 = HTMLNode("span", "Hello", [], {"class": "greeting"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("p", "Sample paragraph", None, None)
        expected_repr = "HTMLNode(p, Sample paragraph, None, None)"
        self.assertEqual(repr(node), expected_repr)

    def test_not_equal_different_type(self):
        node = HTMLNode("p", "Sample paragraph", None, None)
        self.assertNotEqual(node, "Not an HTMLNode")

    def test_neq_edge_case(self):
        node = HTMLNode(None, None, None, None)
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()







