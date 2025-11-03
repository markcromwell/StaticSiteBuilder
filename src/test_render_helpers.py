import unittest

from renderers import (
    render_paragraph,
    render_heading,
    render_code,
    render_quote,
    render_unordered_list,
    render_ordered_list,
)


class TestRenderHelpers(unittest.TestCase):
    def test_render_paragraph(self):
        node = render_paragraph("This is **bold** and _italic_")
        self.assertEqual(node.to_html(), "<p>This is <b>bold</b> and <i>italic</i></p>")

    def test_render_heading(self):
        node = render_heading("## Hello **World**")
        self.assertEqual(node.to_html(), "<h2>Hello <b>World</b></h2>")

    def test_render_code(self):
        block = "```\nprint('x')\n```"
        node = render_code(block)
        self.assertEqual(node.to_html(), "<pre><code>print('x')\n</code></pre>")

    def test_render_quote(self):
        node = render_quote("> This is **quoted**")
        # blockquote contains inline content directly (no inner <p>)
        self.assertEqual(node.to_html(), "<blockquote>This is <b>quoted</b></blockquote>")

    def test_render_unordered_list(self):
        node = render_unordered_list("- one\n- **two**")
        self.assertEqual(node.to_html(), "<ul><li>one</li><li><b>two</b></li></ul>")

    def test_render_ordered_list(self):
        node = render_ordered_list("1. first\n2. **second**")
        self.assertEqual(node.to_html(), "<ol><li>first</li><li><b>second</b></li></ol>")


if __name__ == '__main__':
    unittest.main()
