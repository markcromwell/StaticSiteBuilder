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
        title = extract_title(md)
        self.assertIsNone(title)

    def test_title_with_trailing_spaces(self):
        md = """# Another Title 
Content follows."""
        title = extract_title(md)
        self.assertEqual(title, "Another Title")

            
if __name__ == '__main__':
    unittest.main()
