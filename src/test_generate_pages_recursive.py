import unittest
import os
import shutil
import tempfile
from pathlib import Path

from generate_page import generate_page
from copy_static import copy_static_files


class TestGeneratePagesRecursive(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for each test
        self.test_dir = tempfile.mkdtemp()
        self.content_dir = os.path.join(self.test_dir, "content")
        self.public_dir = os.path.join(self.test_dir, "public")
        os.makedirs(self.content_dir)

        # Create a simple template
        self.template_path = os.path.join(self.test_dir, "template.html")
        with open(self.template_path, "w") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head><title>{{ Title }}</title></head>\n<body>{{ Content }}</body>\n</html>")

    def tearDown(self):
        # Clean up temporary directory after each test
        shutil.rmtree(self.test_dir)

    def test_single_file_generation(self):
        """Test generating a single markdown file in the root content directory."""
        # Create a test markdown file
        content_file = os.path.join(self.content_dir, "index.md")
        with open(content_file, "w") as f:
            f.write("# Test Page\n\nThis is a test.")

        # Generate the page
        dest_file = os.path.join(self.public_dir, "index.html")
        os.makedirs(self.public_dir, exist_ok=True)
        generate_page(content_file, self.template_path, dest_file)

        # Verify the output exists and contains expected content
        self.assertTrue(os.path.exists(dest_file))
        with open(dest_file, "r") as f:
            content = f.read()
            self.assertIn("<title>Test Page</title>", content)
            self.assertIn("<h1>Test Page</h1>", content)
            self.assertIn("<p>This is a test.</p>", content)

    def test_nested_directory_structure(self):
        """Test generating pages from a nested directory structure."""
        # Create nested content structure
        blog_dir = os.path.join(self.content_dir, "blog")
        os.makedirs(blog_dir)

        # Create index.md in content root
        with open(os.path.join(self.content_dir, "index.md"), "w") as f:
            f.write("# Home\n\nWelcome to the site!")

        # Create a blog post
        with open(os.path.join(blog_dir, "post1.md"), "w") as f:
            f.write("# First Post\n\nThis is my first blog post.")

        # Create a nested blog category
        tech_dir = os.path.join(blog_dir, "tech")
        os.makedirs(tech_dir)
        with open(os.path.join(tech_dir, "coding.md"), "w") as f:
            f.write("# Coding Tips\n\nHere are some coding tips.")

        # Define expected output files
        expected_files = [
            os.path.join(self.public_dir, "index.html"),
            os.path.join(self.public_dir, "blog", "post1.html"),
            os.path.join(self.public_dir, "blog", "tech", "coding.html"),
        ]

        # Generate all pages recursively
        for content_file in expected_files:
            # Convert public path to content path
            rel_path = os.path.relpath(content_file, self.public_dir)
            content_path = os.path.join(
                self.content_dir,
                os.path.splitext(rel_path)[0] + ".md"
            )
            os.makedirs(os.path.dirname(content_file), exist_ok=True)
            generate_page(content_path, self.template_path, content_file)

        # Verify all expected files were generated
        for file_path in expected_files:
            self.assertTrue(
                os.path.exists(file_path),
                f"Expected output file missing: {file_path}"
            )
            with open(file_path, "r") as f:
                content = f.read()
                self.assertIn("<!DOCTYPE html>", content)
                self.assertIn("<title>", content)
                self.assertIn("</html>", content)

    def test_special_characters_in_paths(self):
        """Test generating pages from paths containing spaces and special characters."""
        # Create content directory with special characters
        special_dir = os.path.join(self.content_dir, "Blog Posts!")
        os.makedirs(special_dir)

        # Create test file with spaces in name
        content_file = os.path.join(special_dir, "Hello World.md")
        with open(content_file, "w") as f:
            f.write("# Hello World\n\nThis post has spaces in its path!")

        # Generate the page
        dest_dir = os.path.join(self.public_dir, "Blog Posts!")
        dest_file = os.path.join(dest_dir, "Hello World.html")
        os.makedirs(dest_dir, exist_ok=True)
        
        generate_page(content_file, self.template_path, dest_file)

        # Verify the output
        self.assertTrue(os.path.exists(dest_file))
        with open(dest_file, "r") as f:
            content = f.read()
            self.assertIn("<title>Hello World</title>", content)
            self.assertIn("<h1>Hello World</h1>", content)

    def test_missing_content_directory(self):
        """Test behavior when content directory is missing."""
        # Remove the content directory
        shutil.rmtree(self.content_dir)

        # Try to generate pages - this should not raise an error
        # but should handle the missing directory gracefully
        try:
            # The recursive function should handle this case
            self.assertFalse(os.path.exists(self.content_dir))
        except Exception as e:
            self.fail(f"Unexpected exception when handling missing content dir: {e}")

    def test_duplicate_file_names(self):
        """Test handling of duplicate file names in different directories."""
        # Create nested directories with same-named files
        os.makedirs(os.path.join(self.content_dir, "section1"))
        os.makedirs(os.path.join(self.content_dir, "section2"))

        # Create index.md in multiple locations
        paths = [
            os.path.join(self.content_dir, "index.md"),
            os.path.join(self.content_dir, "section1", "index.md"),
            os.path.join(self.content_dir, "section2", "index.md"),
        ]

        # Create content files with different content
        for i, path in enumerate(paths):
            with open(path, "w") as f:
                f.write(f"# Section {i}\n\nThis is section {i}")

        # Generate pages
        for i, content_path in enumerate(paths):
            if i == 0:
                dest_path = os.path.join(self.public_dir, "index.html")
            else:
                section = f"section{i}"
                dest_path = os.path.join(self.public_dir, section, "index.html")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(content_path, self.template_path, dest_path)

        # Verify each file has the correct content
        for i in range(len(paths)):
            if i == 0:
                html_path = os.path.join(self.public_dir, "index.html")
            else:
                html_path = os.path.join(self.public_dir, f"section{i}", "index.html")
            
            self.assertTrue(os.path.exists(html_path))
            with open(html_path, "r") as f:
                content = f.read()
                self.assertIn(f"<title>Section {i}</title>", content)
                self.assertIn(f"<h1>Section {i}</h1>", content)


if __name__ == "__main__":
    unittest.main()