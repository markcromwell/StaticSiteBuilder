import unittest

from textnode import markdown_to_html_node


class TestMarkdownToHtmlNodeExtra(unittest.TestCase):
    def test_heading_rendering(self):
        md = "# Title\n\n## Sub"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Title</h1><h2>Sub</h2></div>")

    def test_blockquote_with_inline_markup(self):
        md = "> This is **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # blockquote contains inline content directly (no inner <p>)
        self.assertEqual(html, "<div><blockquote>This is <b>bold</b></blockquote></div>")

    def test_unordered_list_rendering(self):
        md = "- a\n- b"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>a</li><li>b</li></ul></div>")

    def test_ordered_list_rendering(self):
        md = "1. a\n2. b"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>a</li><li>b</li></ol></div>")

    def test_codeblock_with_language_tag(self):
        md = "```python\nprint('x')\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # our implementation preserves the language token in the inner content
        self.assertEqual(html, "<div><pre><code>python\nprint('x')\n</code></pre></div>")


if __name__ == '__main__':
    unittest.main()
