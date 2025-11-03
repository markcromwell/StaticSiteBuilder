#!/usr/bin/env python3

from textnode import TextNode
from copy_static import copy_static_files
import os


def main():
    """
    Delete anything in the public directory.
    Copy all the static files from static to public.
    Generate a page from content/index.md using template.html and write it to public/index.html.
    """
    # Resolve paths relative to the project root and this src directory so the
    # script works when invoked from the project root or any working directory.
    src_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(src_dir)

    from generage_page import generate_page
    static_src = os.path.join(project_root, "static")
    public_dest = os.path.join(project_root, "public")
    # template.html lives in the src directory
    template_path = os.path.join(src_dir, "template.html")
    content_path = os.path.join(project_root, "content", "index.md")
    output_path = os.path.join(project_root, "public", "index.html")

    # Resolved paths (no debug print) — generate_page will be called with absolute paths.

    copy_static_files(static_src, public_dest)
    generate_page(content_path, template_path, output_path)
    

if __name__ == "__main__":
    main()