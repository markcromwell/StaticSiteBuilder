import unittest
from generage_page import generate_page

class TestExtractTitle(unittest.TestCase):
    def test_generate_page_includes_title_and_content(self):
        """
        Test generate_page that takes in 3 arguments:
            from_path, template_path, dest_path

            Those are file paths to the markdown source file, the HTML template file,
            and the destination HTML file to write to. You should create those files as temp files and populate
            them with test data. Then call generate_page with those paths.
        """ 
        import tempfile
        import os
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create markdown source file
            md_path = tmpdir_path / "source.md"
            md_content = "# Test Title\nThis is some test content."
            md_path.write_text(md_content, encoding='utf-8')

            # Create HTML template file
            template_path = tmpdir_path / "template.html"
            template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"
            template_path.write_text(template_content, encoding='utf-8')

            # Destination path
            dest_path = tmpdir_path / "output.html"

            # Call generate_page
            generate_page(str(md_path), str(template_path), str(dest_path))

            # Read the output file and verify contents
            output_content = dest_path.read_text(encoding='utf-8')
            self.assertIn("<title>Test Title</title>", output_content)
            self.assertIn("<h1>Test Title</h1>", output_content)
            self.assertIn("<p>This is some test content.</p>", output_content) 



if __name__ == '__main__':
    unittest.main()

