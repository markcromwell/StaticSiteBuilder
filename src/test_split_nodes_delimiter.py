from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType
import unittest
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        old_nodes = [
            TextNode("Hello, World! This is a test.", TextType.TEXT),
            TextNode("Another node.", TextType.TEXT)
        ]
        delimiter = " "
        text_type = TextType.TEXT

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected_texts = [
            "Hello,",
            " ",
            "World!",
            " ",
            "This",
            " ",
            "is",
            " ",
            "a",
            " ",
            "test.",
            "Another",
             " ",
             "node."
        ]

        self.assertEqual(len(new_nodes), len(expected_texts))
        for new_node, expected_text in zip(new_nodes, expected_texts):
            self.assertIsInstance(new_node, TextNode)
            self.assertEqual(new_node.text, expected_text)
            self.assertEqual(new_node.text_type, text_type)

    def test_split_nodes_delimiter_no_split(self):
        old_nodes = [
            TextNode("NoDelimiterHere", TextType.TEXT)
        ]
        delimiter = " "
        text_type = TextType.TEXT

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], old_nodes[0])

    def test_split_nodes_delimiter_different_type(self):
        old_nodes = [
            TextNode("Hello, World!", TextType.BOLD)
        ]
        delimiter = " "
        text_type = TextType.TEXT

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], old_nodes[0])

    def test_split_nodes_delimiter_multiple_delimiters(self):
        old_nodes = [
            TextNode("One,,Two,,Three", TextType.TEXT)
        ]
        delimiter = ","
        text_type = TextType.TEXT

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected_texts = [
            "One",
            ",",
            ",",
            "Two",
            ",",
            ",",
            "Three"
        ]

        self.assertEqual(len(new_nodes), len(expected_texts))
        for new_node, expected_text in zip(new_nodes, expected_texts):
            self.assertIsInstance(new_node, TextNode)
            self.assertEqual(new_node.text, expected_text)
            self.assertEqual(new_node.text_type, text_type)

    def test_split_nodes_delimiter_bold(self):
        print ("Testing split_nodes_delimiter with BOLD TextType")
        old_nodes = [
        TextNode("Bold **text** here", TextType.BOLD)
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected_texts = [
                "Bold ",
                "**",
                "text",
                "**",
                " here"
        ]

        self.assertEqual(len(new_nodes), len(expected_texts))
        for new_node, expected_text in zip(new_nodes, expected_texts):
            self.assertIsInstance(new_node, TextNode)
            self.assertEqual(new_node.text, expected_text)
            self.assertEqual(new_node.text_type, text_type)