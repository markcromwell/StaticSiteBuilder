import unittest

from textnode import block_to_block_type, BlockType


class TestBlockToBlockTypeExtra(unittest.TestCase):
    def test_heading_without_space_is_paragraph(self):
        self.assertEqual(block_to_block_type('#NoSpace'), BlockType.PARAGRAPH)

    def test_heading_with_trailing_hashes(self):
        self.assertEqual(block_to_block_type('## Title ##'), BlockType.HEADING)

    def test_ordered_list_with_leading_space_on_line_is_paragraph(self):
        block = '1. one\n 2. two'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
