#!/usr/bin/env python3

from textnode import TextNode
from copy_static import copy_static_files


def main():
    copy_static_files("static", "public")

if __name__ == "__main__":
    main()