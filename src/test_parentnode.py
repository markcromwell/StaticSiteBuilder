from parentnode import ParentNode
from leafnode import LeafNode
import unittest


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode("div", [], {"class": "container"})
        node2 = ParentNode("div", [], {"class": "container"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = ParentNode("div", [], {"class": "container"})
        node2 = ParentNode("span", [], {"class": "container"})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = ParentNode("ul", [], None)
        expected_repr = "ParentNode(ul, [], None)"
        self.assertEqual(repr(node), expected_repr)

    def test_not_equal_different_type(self):
        node = ParentNode("ul", [], None)
        self.assertNotEqual(node, "Not a ParentNode")

    def test_to_html_with_props(self):
        child1 = LeafNode("li", "Item 1")
        child2 = LeafNode("li", "Item 2")
        node = ParentNode("ul", [child1, child2], {"id": "list"})
        expected_html = '<ul id="list"><li>Item 1</li><li>Item 2</li></ul>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_props(self):
        child1 = LeafNode("li", "Item 1")
        child2 = LeafNode("li", "Item 2")
        node = ParentNode("ul", [child1, child2])
        expected_html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_no_tag_raises(self):
        child = LeafNode("li", "Item")
        node = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()