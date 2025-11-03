import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_with_title(self):
        md = """# My Title  
This is some content."""
        title = extract_title(md)
        self.assertEqual(title, "My Title") 

    def test_without_title(self):
        md = """This is some content without a title."""

        with self.assertRaises(ValueError) as cm:
            extract_title(md)

        exception = cm.exception
        self.assertEqual(str(exception), "No title found in markdown content.")

    def test_title_with_trailing_spaces(self):
        md = """# Another Title 
Content follows."""
        title = extract_title(md)
        self.assertEqual(title, "Another Title")


if __name__ == '__main__':
    unittest.main()
