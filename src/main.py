#!/usr/bin/env python3

from textnode import TextNode


def main():
    print("hello world")
    new_text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev)")

    print (new_text_node)

if __name__ == "__main__":
    main()