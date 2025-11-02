import unittest

from textnode import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_levels_1_to_6(self):
        for i in range(1, 7):
            line = "#" * i + " Heading"
            self.assertEqual(block_to_block_type(line), BlockType.HEADING)

    def test_heading_too_many_hashes_is_paragraph(self):
        line = "#" * 7 + " Too many"
        self.assertEqual(block_to_block_type(line), BlockType.PARAGRAPH)

    def test_code_block_single_line_fenced(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_missing_end_is_paragraph(self):
        block = "```\nprint('hi')\nnot closed"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiple_lines(self):
        block = "> First line\n> Second line\n> Third"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_fails_if_line_missing_gt(self):
        block = "> First\nSecond"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_simple(self):
        block = "- first\n- second\n- third"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_space_required(self):
        block = "-first\n-second"
        # since there's no space after '-', it's not matched and becomes paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_simple(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_non_starting_one_is_paragraph(self):
        block = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_non_sequential_is_paragraph(self):
        block = "1. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_list_lines_are_paragraph(self):
        block = "- first\n1. second\n- third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_leading_whitespace(self):
        # The function assumes whitespace is stripped; with leading space it should be paragraph
        block = "  # Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_code_block_backticks_at_edges(self):
        # Code block must start with ``` and end with ``` exactly on their lines
        block = "```\ncode line\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)


if __name__ == '__main__':
    unittest.main()
