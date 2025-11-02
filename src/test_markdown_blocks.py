import unittest

from textnode import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_double_newline(self):
        md = "First paragraph\n\nSecond paragraph"
        self.assertEqual(markdown_to_blocks(md), ["First paragraph", "Second paragraph"]) 

    def test_no_leading_newline(self):
        md = "First\n\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"]) 

    def test_leading_blank_lines(self):
        md = "\n\nFirst\n\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"]) 

    def test_windows_crlf(self):
        md = "First\r\n\r\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"]) 

    def test_multiple_blank_lines(self):
        md = "First\n\n\n\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"]) 

    def test_whitespace_only_separator(self):
        md = "First\n  \nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"]) 

    def test_single_paragraph(self):
        md = "Only one paragraph with no blank lines"
        self.assertEqual(markdown_to_blocks(md), [md])

    def test_only_whitespace_returns_empty(self):
        md = "   \n  \n"
        self.assertEqual(markdown_to_blocks(md), [])


if __name__ == '__main__':
    unittest.main()
