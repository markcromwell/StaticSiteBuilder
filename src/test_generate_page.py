import unittest
import tempfile
import os
from pathlib import Path
from generate_page import generate_page


class TestGeneratePage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir_path = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def create_files(self, md_content, template_content):
        md_path = self.tmpdir_path / "source.md"
        template_path = self.tmpdir_path / "template.html"
        dest_path = self.tmpdir_path / "output.html"

        md_path.write_text(md_content, encoding='utf-8')
        template_path.write_text(template_content, encoding='utf-8')

        return md_path, template_path, dest_path

    def test_basic_title_and_content(self):
        """Test basic markdown with title and paragraph"""
        md_path, template_path, dest_path = self.create_files(
            "# Test Title\n\nThis is some test content.",
            "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        )

        generate_page("", str(md_path), str(template_path), str(dest_path))
        
        output_content = dest_path.read_text(encoding='utf-8')
        self.assertIn("<title>Test Title</title>", output_content)
        self.assertIn("<h1>Test Title</h1>", output_content)
        self.assertIn("<p>This is some test content.</p>", output_content)

    def test_complex_markdown_content(self):
        """Test markdown with multiple block types"""
        md_content = """# Complex Page
        
This is a paragraph with **bold** and _italic_ text.

## Second Level Heading

1. First item
2. Second item

> This is a blockquote
> with multiple lines

```python
def hello():
    print("Hello world")
```"""
        
        md_path, template_path, dest_path = self.create_files(
            md_content,
            "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        )

        generate_page("", str(md_path), str(template_path), str(dest_path))
        
        output = dest_path.read_text(encoding='utf-8')
        self.assertIn("<h1>Complex Page</h1>", output)
        self.assertIn("<h2>Second Level Heading</h2>", output)
        self.assertIn("<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>", output)
        self.assertIn("<ol>", output)
        self.assertIn("<li>First item</li>", output)
        self.assertIn("<blockquote>", output)
        self.assertIn("<pre><code>", output)

    def test_missing_title_raises_error(self):
        """Test that markdown without a title raises ValueError"""
        md_path, template_path, dest_path = self.create_files(
            "Just some content without a title",
            "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
        )

        with self.assertRaises(ValueError) as cm:
            generate_page("", str(md_path), str(template_path), str(dest_path))
        self.assertIn("No title found", str(cm.exception))

    def test_custom_template(self):
        """Test with a more complex template"""
        template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ Title }} - My Blog</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav><a href="/">Home</a></nav>
    <main>
        <article>{{ Content }}</article>
    </main>
    <footer>Copyright 2025</footer>
</body>
</html>"""

        md_path, template_path, dest_path = self.create_files(
            "# Page Title\n\nContent here.",
            template
        )

        generate_page("", str(md_path), str(template_path), str(dest_path))
        
        output = dest_path.read_text(encoding='utf-8')
        self.assertIn("<title>Page Title - My Blog</title>", output)
        self.assertIn("<nav><a href=\"/\">Home</a></nav>", output)
        self.assertIn("<article><h1>Page Title</h1><p>Content here.</p></article>", output)
        self.assertIn("<footer>Copyright 2025</footer>", output)

    def test_nested_output_directory(self):
        """Test generating page in a nested directory structure"""
        md_path, template_path, _ = self.create_files(
            "# Nested Page\n\nContent.",
            "<html><title>{{ Title }}</title><body>{{ Content }}</body></html>"
        )
        
        # Create a nested destination path
        dest_path = self.tmpdir_path / "posts" / "2025" / "11" / "page.html"

        generate_page("", str(md_path), str(template_path), str(dest_path))
        
        self.assertTrue(dest_path.exists())
        self.assertTrue(dest_path.is_file())
        content = dest_path.read_text(encoding='utf-8')
        self.assertIn("<h1>Nested Page</h1>", content)


if __name__ == '__main__':
    unittest.main()


