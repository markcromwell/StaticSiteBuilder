#!/usr/bin/env python3

from textnode import TextNode
from copy_static import copy_static_files


def main():
    """
    Delete anything in the public directory.
    Copy all the static files from static to public.
    Generate a page from content/index.md using template.html and write it to public/index.html.
    """
    from generage_page import generate_page
    copy_static_files("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    

if __name__ == "__main__":
    main()