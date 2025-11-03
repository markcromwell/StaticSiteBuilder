#!/usr/bin/env python3

from textnode import TextNode
from copy_static import copy_static_files
import os
import sys



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

    from generate_page import generate_page, generate_pages_recursive
    static_src = os.path.join(project_root, "static")
    public_dest = os.path.join(project_root, "docs")
    # template.html lives in the src directory
    template_path = os.path.join(src_dir, "template.html")
    # Use content directory and public directory for recursive generation
    content_path = os.path.join(project_root, "content")
    output_path = os.path.join(project_root, "docs")

    # Resolved paths (no debug print) — generate_page will be called with absolute paths.

    copy_static_files(static_src, public_dest)
    # Generate all pages from the content directory into the public directory

    # Use base path for href/src rewriting (default: empty string for root)
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive(basepath, content_path, template_path, output_path)
    

if __name__ == "__main__":
    main()