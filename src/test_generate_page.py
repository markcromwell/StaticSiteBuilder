import unittest
from generage_page import generate_page

class TestExtractTitle(unittest.TestCase):
    def test_generate_page_includes_title_and_content(self):
        title = "Sample Title"
        content = "<p>This is sample content.</p>"
        page = generate_page(title, content)
        expected_page = f"""<html>  
<head><title>{title}</title></head>
<body>
{content}
</body>
</html>"""
        self.assertEqual(page, expected_page)


if __name__ == '__main__':
    unittest.main()

