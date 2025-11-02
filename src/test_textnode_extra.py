import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_image, split_nodes_link
from leafnode import LeafNode


class TestTextNodeExtra(unittest.TestCase):
    def test_all_text_types_to_htmlnode(self):
        cases = [
            (TextType.TEXT, None, 'LeafNode(None, hello, None)'),
            (TextType.BOLD, None, 'LeafNode(b, hello, None)'),
            (TextType.ITALIC, None, 'LeafNode(i, hello, None)'),
            (TextType.CODE, None, 'LeafNode(code, hello, None)'),
            (TextType.LINK, 'https://x', "LeafNode(a, hello, {'href': 'https://x'})"),
            (TextType.IMAGE, 'https://img', "LeafNode(img, None, {'src': 'https://img', 'alt': 'hello'})"),
        ]

        for ttype, url, expected in cases:
            with self.subTest(ttype=ttype):
                node = TextNode('hello', ttype, url)
                html = text_node_to_html_node(node)
                self.assertEqual(repr(html), expected)

    def test_split_nodes_image_adjacent(self):
        # Two adjacent image markdowns
        s = '![a](u1)![b](u2)'
        old_nodes = [TextNode(s, TextType.IMAGE)]
        new_nodes = split_nodes_image(old_nodes)
        # Implementation produces 4 nodes: alt1, url1, alt2, url2
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, 'a')
        self.assertEqual(new_nodes[1].text, 'u1')
        self.assertEqual(new_nodes[2].text, 'b')
        self.assertEqual(new_nodes[3].text, 'u2')

    def test_split_nodes_image_no_match_converts_to_text(self):
        # If TextType.IMAGE but no markdown-like pattern, implementation will turn node into TEXT
        s = 'not an image'
        old_nodes = [TextNode(s, TextType.IMAGE)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, s)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_image_with_extra_text(self):
        s = 'start ![alt](http://u) end'
        old_nodes = [TextNode(s, TextType.IMAGE)]
        new_nodes = split_nodes_image(old_nodes)
        expected = [
            TextNode('start ', TextType.TEXT),
            TextNode('alt', TextType.TEXT),
            TextNode('http://u', TextType.TEXT),
            TextNode(' end', TextType.TEXT),
        ]
        self.assertListEqual([(n.text, n.text_type) for n in expected], [(n.text, n.text_type) for n in new_nodes])

    def test_split_nodes_link_basic_and_edgecases(self):
        # basic
        s = 'before [link](https://x) after'
        new_nodes = split_nodes_link([TextNode(s, TextType.LINK)])
        texts = [n.text for n in new_nodes]
        self.assertEqual(texts, ['before ', 'link', 'https://x', ' after'])

        # adjacent links
        s2 = '[a](u1)[b](u2)'
        new_nodes2 = split_nodes_link([TextNode(s2, TextType.LINK)])
        texts2 = [n.text for n in new_nodes2 if n.text != '']
        self.assertIn('a', texts2)
        self.assertIn('u1', texts2)
        self.assertIn('b', texts2)
        self.assertIn('u2', texts2)

    def test_split_nodes_link_malformed(self):
        # malformed link becomes a TEXT node content (same behavior as images)
        s = 'not a [valid link'
        new_nodes = split_nodes_link([TextNode(s, TextType.LINK)])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, s)

    def test_unicode_and_newline_in_alt_and_url(self):
        s = 'prefix ![unicøde åß](https://example.com/path\nmore) suffix'
        new_nodes = split_nodes_image([TextNode(s, TextType.IMAGE)])
        # ensure unicode alt and url parts extracted
        texts = [n.text for n in new_nodes]
        self.assertTrue(any('unicøde' in t for t in texts))
        self.assertTrue(any('https://example.com' in t for t in texts))

    def test_textnode_eq_and_repr_special(self):
        node = TextNode('a, b', TextType.TEXT, None)
        node2 = TextNode('a, b', TextType.TEXT, None)
        self.assertEqual(node, node2)
        # repr should contain the text and type; exact formatting already tested elsewhere
        r = repr(node)
        self.assertIn('a, b', r)
        self.assertIn('TextType.TEXT', r)


if __name__ == '__main__':
    unittest.main()
