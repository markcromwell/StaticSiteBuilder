import unittest

from textnode import text_to_children
from parentnode import ParentNode


class TestTextToChildren(unittest.TestCase):
    def test_basic_inline(self):
        children = text_to_children("This is **bold** and _italic_")
        node = ParentNode('p', children)
        self.assertEqual(node.to_html(), "<p>This is <b>bold</b> and <i>italic</i></p>")

    def test_link_and_image(self):
        children = text_to_children("Click [here](https://x) and an ![alt](https://img.png)")
        node = ParentNode('p', children)
        self.assertEqual(node.to_html(), '<p>Click <a href="https://x">here</a> and an <img src="https://img.png" alt="alt"/></p>')


if __name__ == '__main__':
    unittest.main()
