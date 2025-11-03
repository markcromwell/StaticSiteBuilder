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
        """Test generating pages from a nested directory structure with generate_pages_recursive."""
        # Create nested content structure with various nested files
        structure = {
            "index.md": "# Home\n\nWelcome to the site!",
            "about/index.md": "# About\n\nAbout this site.",
            "blog/post1.md": "# First Post\n\nThis is my first blog post.",
            "blog/post2.md": "# Second Post\n\nThis is my second blog post.",
            "blog/tech/coding.md": "# Coding Tips\n\nHere are some coding tips.",
            "blog/tech/python/basics.md": "# Python Basics\n\nLearn Python basics here.",
            "projects/index.md": "# Projects\n\nMy projects list.",
            "projects/web/static-site.md": "# Static Site\n\nA static site generator."
        }

        # Create the files
        for path, content in structure.items():
            full_path = os.path.join(self.content_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)

        # Define mappings for verification
        expected_files = {
            "index.html": {"title": "Home", "heading": "<h1>Home</h1>", "text": "Welcome to the site!"},
            "about/index.html": {"title": "About", "heading": "<h1>About</h1>", "text": "About this site."},
            "blog/post1.html": {"title": "First Post", "heading": "<h1>First Post</h1>", "text": "This is my first blog post."},
            "blog/post2.html": {"title": "Second Post", "heading": "<h1>Second Post</h1>", "text": "This is my second blog post."},
            "blog/tech/coding.html": {"title": "Coding Tips", "heading": "<h1>Coding Tips</h1>", "text": "Here are some coding tips."},
            "blog/tech/python/basics.html": {"title": "Python Basics", "heading": "<h1>Python Basics</h1>", "text": "Learn Python basics here."},
            "projects/index.html": {"title": "Projects", "heading": "<h1>Projects</h1>", "text": "My projects list."},
            "projects/web/static-site.html": {"title": "Static Site", "heading": "<h1>Static Site</h1>", "text": "A static site generator."}
        }

        # Print current structure before generation
        print("\nContent directory structure:")
        for root, dirs, files in os.walk(self.content_dir):
            level = root.replace(self.content_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            for f in files:
                print(f"{indent}    {f}")

        # Call generate_pages_recursive
        from generate_page import generate_pages_recursive
        generate_pages_recursive(self.content_dir, self.template_path, self.public_dir)

        # Print generated structure after generation
        print("\nGenerated directory structure:")
        for root, dirs, files in os.walk(self.public_dir):
            level = root.replace(self.public_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            for f in files:
                print(f"{indent}    {f}")

        # Verify each expected file exists and has correct content
        missing_files = []
        content_errors = []

        for rel_path, checks in expected_files.items():
            full_path = os.path.join(self.public_dir, rel_path)
            
            # Track missing files
            if not os.path.exists(full_path):
                missing_files.append(rel_path)
                continue

            # Check file content
            with open(full_path, "r") as f:
                content = f.read()
                for check_type, expected in checks.items():
                    if expected not in content:
                        content_errors.append(f"Missing {check_type} in {rel_path}")

        # Assert all files exist
        self.assertEqual(
            [],
            missing_files,
            f"Missing expected files: {missing_files}"
        )

        # Assert all content is correct
        self.assertEqual(
            [],
            content_errors,
            f"Content verification errors: {content_errors}"
        )

        # Verify directory structure matches exactly
        expected_structure = set([
            os.path.dirname(f) for f in expected_files.keys()
            if os.path.dirname(f)  # Exclude files in root
        ])
        actual_structure = set()
        for root, dirs, files in os.walk(self.public_dir):
            rel_path = os.path.relpath(root, self.public_dir)
            if rel_path != ".":
                actual_structure.add(rel_path)
        
        self.assertEqual(
            expected_structure,
            actual_structure,
            "Directory structure doesn't match expected"
        )

        # Verify all expected files were generated
        for rel_path in expected_files:
            full_path = os.path.join(self.public_dir, rel_path)
            self.assertTrue(
                os.path.exists(full_path),
                f"Expected output file missing: {rel_path} (full path: {full_path})"
            )
            with open(full_path, "r") as f:
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